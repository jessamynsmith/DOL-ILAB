#!/usr/bin/python

"""Parses all country files specified in <input_path> and writes the output as
JSON to <output_file>.

Usage: ./run.py --input_path <directory> --output_file <file>

The input_path should contain HTML files. Note that the parser expects the HTML
to be formatted by Word. The Department of Labor country profile documents should
be opened in Word and saved as a Web Page.

The JSON output will have this form:
[{
  advancement_level: string,
  country: string,
  description: string (A paragraph about the country),
  sources: [{
    number: string (The index of the source),
    text: string
  }],
  tables: [{
    footnotes: [
      symbol: string (The symbol of the footnote),
      text: string
    ],
    summary: string (A summary sentence about the table),
    title: string,
    /* There will be one of the following lists. */
    items: [{
      descriptions: [{
        sources: string, (The source of the information in text)
        text: string (A description of the item)
      }],
      name: string (The name of the item in the list)
    }],
    areas: [{
      actions: [{
        action: string (A description of the action),
        years: string (Year(s), which may be separated by commas or an m-dash)
      }],
      area: string (The area corresponding to these actions)
    }],
    conventions: [{
      ratification: bool (True if the convention has been ratified),
      title: string (The title of the convetion)
    }],
    sectors: [{
      activities: [{
        name: string (The name of the activities; may be a comma separated list),
        sources: string (The sources of the activity text)
      }],
      sector: string (A sector in which the activities fall)
    }],
    standards: [{
      age: string (The age corresponding to the standard; may be a range),
      enacted: string (Yes, No, or N/A),
      related_legislation: [{
        legislation: string (Related legislation to the standard),
        sources: string (Sources for the related legislation)
      }],
      title: string
    }],
  }]
}]
"""

import fnmatch
import getopt
import json
import os
import sys

from parser import Parser

def print_usage():
  print 'Usage: main.py -i <input_path> -o <output_file>'

def main(argv):
  try:
    opts, args = getopt.getopt(argv, 'hio:', ['input_path=', 'output_file='])
  except getopt.GetoptError:
    print_usage()
    sys.exit(2)

  input_path = output_path = None
  for opt, arg in opts:
    if opt == '-h' or opt == '--help':
      print_usage()
      sys.exit()
    elif opt in ('-i', '--input_path'):
      input_path = arg
    elif opt in ('-o', '--output_file'):
      output_file = arg

  if not input_path or not output_file:
    print_usage()
    sys.exit(2)

  # TODO: Check valid input path and output file.
  if not (output_file.endswith('.json'):
    print 'Output file must be .json'
    print_usage()
    sys.exit(2)

  parser = Parser()
  country_details = []
  # Run on all HTML files within the source_data/countries directory.
  # TODO: Handle file patterns.
  filenames = []
  if os.path.isdir(input_path):
    for root, dirnames, filenames in os.walk(input_path):
      for filename in fnmatch.filter(filenames, '*.html'):
        filenames.append(os.path.join(root, filename))
  else:
    assert(os.path.isfile(input_path))
    filenames.append(input_path)

  for filename in filenames:
    with open(filename, 'r') as f:
      country_details.append(parser.parse(filename))

  with open(output_file, 'w') as f:
    json.dump(country_details, f, indent=2, sort_keys=True)

if __name__ == '__main__':
  main(sys.argv[1:])
