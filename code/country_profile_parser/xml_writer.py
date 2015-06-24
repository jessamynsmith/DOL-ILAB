import re
from lxml import etree

def add_element(tag, text=None, attrs={}):
  '''Creates an XML element with the optional text and attributes.

  Args:
    tag: The name of the element.
    text: The inner text of the element.
    attrs: A dictionary containing key value pairs.

  Returns:
    The newly created XML element.
  '''
  elem = etree.Element(tag)
  if text:
    elem.text = text
  for key, value in attrs.items():
    if value:
      elem.set(key, value)
  return elem

def convert_value_to_xml(elem, tag, value):
  '''Converts a value to an XML attribute, element, or elements.

  Args:
    elem: The element to modify.
    tag: The name of the element or attribute to create.
    text: The value for the element. May be a string, boolean, dictionary, or
       list.
  '''
  if isinstance(value, str) or isinstance(value, unicode):
    elem.append(add_element(tag, value))
  elif isinstance(value, bool):
    elem.set(tag, '1' if value else '0')
  elif isinstance(value, dict):
    convert_dict_to_xml(elem, tag, value)
  elif isinstance(value, list):
    # Changes pluralized tag names to the singular, per XML convention.
    if tag.endswith('ies'):
      tag = re.sub(r'ies$', 'y', tag)
    elif tag.endswith('s'):
      tag = re.sub('s$', '', tag)
    for item in value:
      convert_value_to_xml(elem, tag, item)
  else:
    assert(False), ('Unknown element type', type(value))

def convert_dict_to_xml(parent, tag, dictionary):
  '''Converts a dictionary to an XML element, appending it to the parent.
  
  Each key in the dictionary is made a child element of the root element.

  Args:
    parent: The parent element to which to append the new element.
    tag: The name of the root element.
    dictionary: Key-value pairs to convert to children elements.
  '''
  elem = add_element(tag)
  for key, value in dictionary.items():
    children = convert_value_to_xml(elem, key, value)
  parent.append(elem)

def build_tree(root_tag, item_tag, items):
  '''Builds a tree out of a list of dictionaries.

  Args:
    root_tag: The name of the root element.
    item_tag: The name of the tag for each item element.
    items: A list of dictionaries.

  Returns:
    The tree root.
  '''
  root = add_element(root_tag)
  for item in items:
    convert_dict_to_xml(root, item_tag, item)
  return root

def write_to_file(country_details, f):
  '''Writes the country details object to a file.
  
  Args:
    country_details: A list of dictionaries, where each dictionary describes a
      country.
    f: A file, opened for writing.
  '''
  root = build_tree('country_profiles', 'country', country_details)
  # Now special-case the content/paragraph element. Change these from being
  # structured as
  # <content header="1"><paragraph>TEXT 1</paragraph></content>
  # <content header="0"><paragraph>TEXT 2</paragraph></content>
  # to
  # <content>
  #  <paragraph header="1">TEXT 1</paragraph>
  #  <paragraph header="0">TEXT 2</paragraph>
  # </content>
  section_elems = root.findall('.//section')
  for section_elem in section_elems:
    content_elems = section_elem.findall('./content')
    if len(content_elems):
      # Insert a single, new content element to be the parent of all paragraph
      # elements.
      new_content_elem = add_element('content')
      content_elems[-1].addnext(new_content_elem)
      for content_elem in content_elems:
        # Remove the old content element from the section as it is replaced by
        # the new content element above.
        section_elem.remove(content_elem)
        paragraph_elem = content_elem.find('./paragraph')
        # Move the header attribute from the old content element to the
        # paragraph element.
        paragraph_elem.set('header', content_elem.get('header'))
        # Move each paragraph element to be children of the single, new
        # content element.
        new_content_elem.append(paragraph_elem)
  tree = etree.ElementTree(root)
  tree.write(f, pretty_print=True)
