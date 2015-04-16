# -*- coding: utf-8 -*-

from lxml import etree
import re

### Regular expressions used to parse text within the file.

# A table heading, e.g. "Table 1. Statistics on Children’s Work and Education".
TABLE_TITLE_RE = re.compile('Table (\d+)\. (.*)')

# Text followed by source information, e.g. "Mollusk harvesting (18, 34)" where
# 18 and 34 are the sources.
TEXT_SOURCE_RE = re.compile('(.+) ?\(([^)]+)\)$')

# Footnotes below a table, e.g. "* Evidence of this activity is limited and/or the
# extent of the problem is unknown." There are only three known footnote symbols,
# *, †, and ‡.
NOTE_RE = re.compile(u'([*\u2020\u2021]+) (.*)')

# The source definition, e.g. "152.     ILO. Principais Resultados da PNAD 2009:
# Tendências e Desafios. Geneva; October 27, 2010. http://bit.ly/12bzkzX." The
# source is split into its index and text.
SOURCE_RE = re.compile(u'(\d+)\.\s+(.*)')

# The valild values for the advancement levels, used for checking that the
# country info is correct.
ADVANCEMENT_LEVELS = [
  'Significant Advancement',
  'Moderate Advancement',
  'Minimal Advancement',
  'No Advancement',
  'No Assessment',
]

class Parser:
  def __init__(self):
    # Functions that parse an individual table, keyed by the first three words
    # of the table's title.
    self.table_parsers = {
      # Statistics on Children’s Work and Education
      'statistics on childrens': self.work_and_education,
      # Overview of Children’s Work by Sector and Activity
      'overview of childrens': self.sector_and_activity,
      # Ratification of International Conventions on Child Labor
      'ratification of international': self.international_conventions,
      # Laws and Regulations Related to Child Labor
      'laws and regulations': self.laws_and_regulations,
      # Agencies Responsible for Child Labor Law Enforcement
      'agencies responsible for': self.item_with_description_table,
      # Mechanisms to Coordinate Government Efforts on Child Labor
      'mechanisms to coordinate': self.item_with_description_table,
      # Policies Related to Child Labor
      'policies related to': self.item_with_description_table,
      # Social Programs to Address Child Labor
      'social programs to': self.item_with_description_table,
      # Suggested Government Actions to Eliminate Child Labor, Including
      # its Worst Forms  (or)
      # Suggested Government Actions to Prevent Child Labor, Including
      # its Worst Forms
      'suggested government actions': self.suggested_government_actions,
    }

    self.parser = etree.HTMLParser()

  def work_and_education(self, table_title, table_elem):
    '''Table 1. Statistics on Children’s Work and Education'''
    # TODO: This table is already available in an Excel spreadsheet, so it is not
    # parsed here.
    pass

  def sector_and_activity(self, table_title, table_elem):
    '''Table 2. Overview of Children’s Work by Sector and Activity'''
    table = {} # dol.items.SectorTable()
    table['title'] = table_title
    table['footnotes'] = self.get_notes(table_elem)
    table['sectors'] = []

    def AddActivityItem(sector_item, activity_elem):
      # Activity items may have sources attached to them.
      activity_item = {} # dol.items.ActivityItem()
      activity_text = self.get_text(activity_elem)
      m = TEXT_SOURCE_RE.match(activity_text)
      if m:
        activity_text, source_text = m.groups()
        activity_item['sources'] = source_text
      else:
        # Some activities may lack a source. See Madagascar.
        print '  No sources found for "%s"' % activity_text
      activity_item['name'] = activity_text.strip()
      sector_item['activities'].append(activity_item)

    sector_item = None
    row_elems = table_elem.findall('.//tr')
    for row_elem in row_elems[1:]:
      cell_elems = row_elem.findall('./td')
      # A row with two cells contains both the sector name and a group of
      # activities. A row with one cell contains only a group of activities which
      # is part of the previously listed sector.
      if len(cell_elems) == 2:
        # When there are two cells, the first contains the sector and the second
        # a list of activities. Create a new sector item and add the activities to
        # that item.
        sector_elem, activity_elem = cell_elems
        sector_item = {} # dol.items.SectorItem()
        sector_item['sector'] = self.get_text(sector_elem)
        sector_item['activities'] = []
        table['sectors'].append(sector_item)
        AddActivityItem(sector_item, activity_elem)
      elif len(cell_elems) == 1:
        # When there is only one cell, it is a list of activities related to the
        # current sector item.
        AddActivityItem(sector_item, cell_elems[0])

    return table

  def international_conventions(self, table_title, table_elem):
    '''Table 3. Ratification of International Conventions on Child Labor'''
    table = {} # dol.items.InternationalConventionsTable()
    table['title'] = table_title
    table['footnotes'] = self.get_notes(table_elem)
    table['conventions'] = []

    row_elems = table_elem.findall('./tr')
    for row_elem in row_elems[1:]:
      # All rows contain two cells, the first containing the name of the
      # convention and the second stating whether it's been ratified or not, e.g.
      #     "ILO C. 138, Minimum Age" | "[checkmark]".
      cell_elems = row_elem.findall('./td')
      assert(len(cell_elems) == 2)
      convention_cell, ratification_cell = cell_elems
      convention = {} # dol.items.Convention()
      convention['title'] = self.get_text(convention_cell)
      ratification = self.get_text(ratification_cell)
      # A checkmark is used to denote that the convention has been ratified; check
      # only that the cell is non-empty.
      convention['ratification'] = (ratification != '')
      table['conventions'].append(convention)

    return table

  def laws_and_regulations(self, table_title, table_elem):
    '''Table 4. Laws and Regulations Related to Child Labor'''
    table = {} # dol.items.LawsAndRegulationsTable()
    table['title'] = table_title
    table['footnotes'] = self.get_notes(table_elem)
    table['standards'] = []

    row_elems = table_elem.findall('./tr')
    for row_elem in row_elems[1:]:
      # All rows contain four cells: Standard, Yes/No, Age, and Related
      # Related Legislation.
      cell_elems = row_elem.findall('./td')
      if len(cell_elems) != 4:
        # TODO: Handle other cases. See Anguilla, British Virgin Islands.
        continue
      assert(len(cell_elems) == 4), ('Number of cells', len(cell_elems))
      standard = {} # dol.items.Standard()
      standard_cell, enacted_cell, age_cell, related_cell = cell_elems
      standard['title'] = self.get_text(standard_cell)
      standard['enacted'] = self.get_text(enacted_cell)
      age = self.get_text(age_cell)
      if age:
        standard['age'] = age
      # The related legislation should contain source information, so split the
      # source index from the text.
      related_legislation = self.get_text(related_cell)
      m = re.match(TEXT_SOURCE_RE, self.get_text(related_cell))
      if m:
        legislation, sources = m.groups()
        standard['related_legislation'] = {} # dol.items.RelatedLegislation()
        standard['related_legislation']['legislation'] = legislation
        standard['related_legislation']['sources'] = sources
      table['standards'].append(standard)

    return table

  def suggested_government_actions(self, table_title, table_elem):
    '''Table 9. Suggested Government Actions to Eliminate Child Labor, Including
    its Worst Forms'''
    table = {} # dol.items.SuggestedActionsTable()
    table['title'] = table_title
    table['footnotes'] = self.get_notes(table_elem)
    table['areas'] = []

    def AddSuggestedAction(area_item, action_elem, year_elem):
      action_item = {} # dol.items.SuggestedAction()
      action_item['action'] = self.get_text(action_elem)
      action_item['years'] = self.get_text(year_elem)
      area_item['actions'].append(action_item)

    area_item = None
    row_elems = table_elem.findall('.//tr')
    for row_elem in row_elems[1:]:
      # Rows contain two or three cells. A three-columned cell has Area, Suggested
      # Action, and Year(s) Suggested. A two-columned cell has only Suggested
      # Action and Year(s) Suggested, and should use the previously listed Area.
      cell_elems = row_elem.findall('./td')
      # If there are three cells, create a new Area item and add the suggested
      # action to it.
      if len(cell_elems) == 3:
        area_elem, action_elem, year_elem = cell_elems
        area_text = self.get_text(area_elem)
        if area_text:
          area_item = {} # dol.items.Area()
          area_item['area'] = area_text
          area_item['actions'] = []
          table['areas'].append(area_item)
        AddSuggestedAction(area_item, action_elem, year_elem)
      # If there are only two cells, then add a suggested action item to the
      # current area item.
      elif len(cell_elems) == 2:
        action_elem, year_elem = cell_elems
        assert(area_item), self.get_text(action_elem)
        AddSuggestedAction(area_item, action_elem, year_elem)

    return table

  def item_with_description_table(self, table_title, table_elem):
    '''Builds a table with items with descriptions.'''
    table = {} # dol.items.Table()
    table['title'] = table_title
    table['footnotes'] = self.get_notes(table_elem)
    table['items'] = self.get_items_with_description(table_elem)
    return table

  def get_items_with_description(self, table_elem):
    '''Returns the items and their descriptions in this two-column table.'''
    items = []
    row_elems = table_elem.findall('./tr')
    for row_elem in row_elems[1:]:
      # All rows should have two cells, where one is an item and the other is its
      # description.
      cell_elems = row_elem.findall('./td')
      if len(cell_elems) > 2:
        # There may be three cells. See Burundi.
        continue
      assert(len(cell_elems) == 2), ('num elems', len(cell_elems))
      item = {} # dol.items.ItemWithDescription()
      item_cell, desc_cell = cell_elems
      item['name'] = self.get_text(item_cell)
      item['descriptions'] = []
      # There may be multiple descriptions, each separated by a separate set of
      # sources, which are wrapped in parentheses, e.g. "Combats extreme
      # poverty ... million people.(129, 130) The budget rose ... billion
      # in 2013.(19)" Split the text into parts separated by the sources and then
      # pair a description with the subsequent source indices.
      descriptions = re.split('(\.\([\d,\- ]+\))', self.get_text(desc_cell))
      i = 0
      while i < len(descriptions) - 1:
        desc = (descriptions[i] + descriptions[i + 1]).strip()
        i += 2  # Skip ahead two, to account for the description and the sources.
        desc_text, source_text = TEXT_SOURCE_RE.match(desc).groups()
        desc_item = {} # dol.items.Text()
        desc_item['text'] = desc_text.strip()
        desc_item['sources'] = source_text
        item['descriptions'].append(desc_item)
      items.append(item)
    return items

  def get_notes(self, table_elem):
    '''Returns the notes that follow a table.'''
    notes = []
    # The notes are stored in paragraphs immediately following a table. They will
    # start with a symbol, followed by text, and possibly sources.
    # Mimic table_elem.findall('./following-sibling::p').
    note_elems = self.following_elems(table_elem.findall('./../p'), table_elem)
    for note_elem in note_elems:
      m = NOTE_RE.match(self.get_text(note_elem))
      if m:
        symbol, note_text = m.groups()
        source_match = TEXT_SOURCE_RE.match(note_text)
        note_item = {} # dol.items.NoteItem()
        note_item['symbol'] = symbol
        # The sources following a note are optional.
        if source_match:
          note_text, source_text = source_match.groups()
          note_item['sources'] = source_text
        note_item['text'] = note_text
        notes.append(note_item)
      else:
        # A non-matching line indicates the end of the footnotes.
        break
    return notes

  def source_list(self, last_elem):
    '''Extracts the list of sources from the end of the document.'''
    source_list = []
    source_elems = self.following_elems(
      # Find the previous paragraph sibling of this element.
      # Mimic last_elem.xpath('./following::p')
      self.root.findall('.//p'), last_elem)
    for source_elem in source_elems:
      source = self.get_text(source_elem)
      if not source:
        # There may be empty lines at the start or end of the source list.
        continue
      m = SOURCE_RE.match(source)
      if m:
        number, source_text = m.groups()
        if int(number) == len(source_list) + 1:
          # If the number does not match the source list, then there was likely
          # an error in converting from DOC to HTML, leaving something that looks
          # like a source on a line by itself. Treat this as if it were an
          # unmatched source.
          source_item = {} # dol.items.SourceItem()
          source_item['number'] = number
          source_item['text'] = source_text
          source_list.append(source_item)
          continue
      # In the case that this did not match, or that the source number is not in
      # order, concatenate this with the previous line. See Lesotho.
      if source_list:
        source_item = source_list[-1]
        source_item['text'] += '; ' + source
    return source_list

  def get_table_summary(self, table_title_elem):
    '''Returns the description line that comes just before the table title.'''
    elem, text = self.first_elem_with_text(
        self.preceding_elems(
            # Find the previous paragraph sibling of this element.
            # Mimic table_title_elem.xpath('./preceding-sibling::p')
            table_title_elem.findall('./../p'), table_title_elem))
    return text

  def get_text(self, elem):
    '''Extracts the text from an element and clean up whitespace.'''
    if elem is None:
      return ''
    # TODO: Handle embedded lists.
    string = ''.join([t for t in elem.itertext() if t.find('[if ') != 0]).strip()
    string = string.replace(unichr(160), ' ')
    string = re.sub('\s+', ' ', string)
    return unicode(string)

  def check_country(self, country_details):
    '''Verifies that required fields are present the country details item.'''
    assert(country_details['country']), country_details
    assert(country_details['advancement_level']), country_details
    assert(country_details['advancement_level'] in ADVANCEMENT_LEVELS), (
        country_details['advancement_level'])
    assert(country_details['description']), country_details
    assert(country_details['sources']), country_details
    assert(country_details['tables']), country_details
    for table in country_details['tables']:
      assert(table['title']), table
      assert(table['summary']), table

  def first_elem_with_text(self, elems):
    '''Returns the first element with non-empty text from the list of elements.'''
    for elem in elems:
      text = self.get_text(elem)
      if text:
        return elem, text

  def following_elems(self, elems, the_elem):
    '''Returns all elements in elems that follow the_elem.'''
    # Get the index of the last child of the_elem, so that we find the next
    # non-child element.
    the_elem_index = self.all_elems.index(
        [e for e in the_elem.iterchildren()][-1])
    following_elems = []
    for elem in reversed(elems):
      elem_index = self.all_elems.index(elem)
      if elem_index <= the_elem_index:
        return following_elems
      following_elems.insert(0, elem)
    return []

  def preceding_elems(self, elems, the_elems):
    '''Returns all elements in elems that follow the_elem.'''
    the_elem_index = self.all_elems.index(the_elems)
    preceding_elems = []
    for elem in elems:
      elem_index = self.all_elems.index(elem)
      if elem_index >= the_elem_index:
        return preceding_elems
      preceding_elems.insert(0, elem)
    return []

  def parse(self, filename):
    '''Parses a Department of Labor file into structured format.'''
    tree = etree.parse(filename, self.parser)
    self.root = tree.getroot()
    self.all_elems = self.root.findall('.//*')

    country_details = {} # dol.items.CountryDetails()
    country_details['country'] = ''
    # Though the country and assessment levels are ususally in <h1> tags, Saint
    # Helena's is in a <p>. All are nested inside spans, so those are used
    # instead of the <h1>.
    country_span, unused = self.first_elem_with_text(self.root.findall('.//span'))
    country_elem = country_span.getparent()
    country_details['country'] = self.get_text(country_elem)

    advancement_span, unused = self.first_elem_with_text(
        # Find the next span after country_elem.
        # Mimic country_elem.xpath('./following::span').
        self.following_elems(self.root.findall('.//span'), country_elem))
    advancement_elem = advancement_span.getparent()
    country_details['advancement_level'] = self.get_text(advancement_elem)

    print 'Country: %(country)s [%(advancement_level)s]' % country_details

    description_elem, description = self.first_elem_with_text(
        # Find the next p after advancement_elem's parent.
        # Mimic advancement_elem.xpath('./../following::p')
        self.following_elems(self.root.findall('.//p'), advancement_elem))
    country_details['description'] = description

    country_details['tables'] = []

    # Find and parse each of the tale elements.
    table_elems = self.root.findall('.//table')
    for table_elem in table_elems:
      # The table title is the previous paragraph or h1 that is a sibling to the
      # table element.
      # Mimic table_elem.xpath('./preceding-sibling::p[1]')
      preceding_p = self.preceding_elems(table_elem.findall('./../p'), table_elem)
      table_title_elem = preceding_p[0] if len(preceding_p) else None
      table_title_text = self.get_text(table_title_elem)
      if not table_title_text:
        # The title might be in an h1 instead of a p. See Niue (Table 3).
        preceding_h1 = self.preceding_elems(
            # Mimic table_elem.xpath('./preceding-sibling::h1[1]')
            table_elem.findall('./../h1'), table_elem)
        table_title_elem = preceding_h1[0] if len(preceding_h1) else None
        table_title_text = self.get_text(table_title_elem)
      if not table_title_text:
        # There may be a table nested within another table, but that should
        # already have been parsed as part of the previous table. See Thailand.
        print '  Skipping table without title'
        continue

      # Match the table number and title.
      table_number, table_title = re.match(
          TABLE_TITLE_RE, table_title_text).groups()
      table_number_index = int(table_number) - 1

      # Convert the table title into the ID that can be found in the dictionary of
      # table parsers.
      table_id = re.sub('[^\w ]+', '',
          ' '.join(table_title.lower().split(' ')[0:3]))
      if table_id in self.table_parsers:
        table = self.table_parsers[table_id](table_title, table_elem)
        if table:
          table['summary'] = self.get_table_summary(table_title_elem)
          country_details['tables'].append(table)
      else:
        print '  Table not found', table_title, table_id

    # Parse the source list which follows the last table element.
    if table_elem is not None:
      country_details['sources'] = self.source_list(table_elem)

    self.check_country(country_details)
    return country_details

Parser()