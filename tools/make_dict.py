""" Make Dictionary
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import argparse
import os
import sys

def word_to_dictionary(file_in, folder_out):
    #open file with the list of words
    with open(file_in,'r') as f:
        words_dict = {word.rstrip('\n'):number for number, word in enumerate(f, 100)}
  
    #verify if file was given
    f_name=file_in.split('.')
    f_name=f_name[-2].replace('/','')+'.py'

    #verify if folder was given 
    if not folder_out:
      folder_out='./'
    file_out=os.path.join(folder_out,f_name)

    #creates new py file with the dict as a content
    with open(file_out,'w') as f:
      f.write(str(words_dict))
      print("file '{}' was saved in '{}'.".format(f_name,folder_out))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: make_dict word_file [output_dir]")
    if len(sys.argv) == 2:
        word_to_dictionary(sys.argv[1], None)
    else:
        word_to_dictionary(sys.argv[1], sys.argv[2])
