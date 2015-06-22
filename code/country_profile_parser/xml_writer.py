import re
from lxml import etree as ET

def add_element(tag, text=None, attrs={}):
  '''Creates an XML element with the optional text and attributes.

  Args:
    tag: The name of the element.
    text: The inner text of the element.
    attrs: A dictionary containing key value pairs.

  Returns:
    The newly created XML element.
  '''
  elem = ET.Element(tag)
  if text:
    elem.text = text
  for key, value in attrs.items():
    if value:
      elem.set(key, value)
  return elem

def convert_value_to_xml(tag, value):
  '''Converts a value to an XML element, or elements.

  Args:
    tag: The name of the element to create.
    text: The value for the element. May be a string, boolean, dictionary, or
       list.

  Returns:
    An element with the given tag, or if the value was a list, a list of
    elements each with the specified tag name.
  '''
  if isinstance(value, str) or isinstance(value, unicode):
    return add_element(tag, value)
  elif isinstance(value, bool):
    return add_element(tag, '1' if True else '0')
  elif isinstance(value, dict):
    return convert_dict_to_xml(tag, value)
  elif isinstance(value, list):
    # Changes pluralized tag names to the singular, per XML convention.
    if tag.endswith('ies'):
      tag = re.sub(r'ies$', 'y', tag)
    elif tag.endswith('s'):
      tag = re.sub('s$', '', tag)
    return [convert_value_to_xml(tag, item) for item in value]
  else:
    assert(False), ('Unknown element type', type(value))

def convert_dict_to_xml(tag, dictionary):
  '''Converts a dictionary to an XML element.
  
  Each key in the dictionary is made a child element of the root.

  Args:
    tag: The name of the root element.
    dictionary: Key-value pairs to convert to children elements.

  Returns:
    The element created.
  '''
  elem = add_element(tag)
  for key, value in dictionary.items():
    children = convert_value_to_xml(key, value)
    # If the result of convert_value_to_xml is a list, then append each child.
    if isinstance(children, list):
      for child in children:
        elem.append(child)
    else:
      elem.append(children)
  return elem

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
    root.append(convert_dict_to_xml(item_tag, item))
  return root

def write_to_file(country_details, f):
  '''Writes the country details object to a file.
  
  Args:
    country_details: A list of dictionaries, where each dictionary describes a
      country.
    f: A file, opened for writing.
  '''
  root = build_tree('country_profiles', 'country', country_details)
  tree = ET.ElementTree(root)
  tree.write(f, pretty_print=True)
