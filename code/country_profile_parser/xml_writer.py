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
  tree = etree.ElementTree(root)
  tree.write(f, pretty_print=True)
