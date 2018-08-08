""" Make Dictionary
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""
import os
import sys

def word_to_dictionary(file_in, folder_out):
    #open file with the list of words
    with open(file_in,'r') as f:
        first_line = f.readline()
        f.seek(0)
        if len(first_line.split()) == 1:
            words_dict = {word.rstrip('\n'):number for number, word in enumerate(f, 100)}
        else:
            number = 100
            words_dict = {}
            for line in f:
                item=line.split()
                words_dict[item[1]]=number
                number += 1

    words_dict['<PAD>'] = 0
    words_dict['<OUT>'] = 1
    words_dict['<SOS>'] = 2
    words_dict['<EOS>'] = 3
    words_dict['<EMP>'] = 4
    words_dict['<POS>'] = 5
    words_dict['<NEG>'] = 6
  
    f_name='word2int.py'

    #verify if folder was given 
    if not folder_out:
      folder_out='../'
    file_out=os.path.join(folder_out,f_name)

    #creates new py file with the dict as a content
    with open(file_out,'w') as f:
      f.write('word2int =')
      f.write(str(words_dict))
      print("file '{}' was saved in '{}'.".format(f_name,folder_out))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: make_dict word_file [output_dir]")
    if len(sys.argv) == 2:
        word_to_dictionary(sys.argv[1], None)
    else:
        word_to_dictionary(sys.argv[1], sys.argv[2])