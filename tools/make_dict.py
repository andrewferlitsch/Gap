""" Make Dictionary
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import argparse

parser = argparse.ArgumentParser(description='Takes a file with a single word on each line into a dictionary.')
parser.add_argument("--file", help="Name of a person whos face you want to scrape (e.g. \'file.txt\')")
args = parser.parse_args()

def word_to_dictionary(file):
  with open(file,'r') as f:
    test = {word.rstrip("\n"):number for number, word in enumerate(f, 100)}
    return words_dict

file=args.file
words_dict=word_to_dictionary(file)