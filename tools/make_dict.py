""" Make Dictionary
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import argparse
import os

parser = argparse.ArgumentParser(description='Takes a file with a single word on each line into a dictionary.')
parser.add_argument("--file_in", help="file with the list of words (e.g. \'file.txt\')")
parser.add_argument("--folder_out", help="folder where to save the py file (e.g. \'folder\')")
args = parser.parse_args()

def word_to_dictionary(file_in, folder_out):
  #open file with the list of words
  with open(file_in,'r') as f:
    words_dict = {word.rstrip('\n'):number for number, word in enumerate(f, 100)}
  
  #verify if file was given
  if not file_in:
      print("please select a file with --file='file.txt'")
  else:
    f_name=file_in.split('.')
    f_name=f_name[-2].replace('/','')+'.py'

    #verify if folder was given 
    if not folder_out:
      folder_out='./'
    file_out=os.path.join(folder_out,f_name)

    #creates new py file with the dict as a content
    with open(file_out,'w+') as f2:
      f2.write(str(words_dict))
      print("file '{}' was saved in '{}'.".format(f_name,folder_out))

file_in=args.file_in
folder_out=args.folder_out

word_to_dictionary(file_in, folder_out)
