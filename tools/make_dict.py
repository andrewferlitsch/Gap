""" Make Dictionary
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""
import os
import sys

def word_to_dictionary(file, output_dir):
    #open file with the list of words
    with open(file,'r', encoding='utf-8') as f:
        first_line = f.readline()
        f.seek(0)
        if len(first_line.split()) == 1:
            words_dict = {word.rstrip('\n'):number for number, word in enumerate(f, 100) if len(word)>1}
        else:
            line = first_line.split()
            #verify if file has header
            if line[0] not in '.-0123456789':
                next(f)
            words_dict = {line.split()[1]:number for number, line in enumerate(f, 100) if len(line.split()[1])>1}

    words_dict['<PAD>'] = 0
    words_dict['<OUT>'] = 1
    words_dict['<SOS>'] = 2
    words_dict['<EOS>'] = 3
    words_dict['<EMP>'] = 4
    words_dict['<POS>'] = 5
    words_dict['<NEG>'] = 6

    #verify if word2int name 
    lang = file.split('.')[0].split('-')[0]
    if lang != 'en':
        f_name='word2int_{}.py'.format(lang)
    else:
        f_name='word2int_en.py'

    #verify if folder was given 
    if not output_dir:
        output_dir='../'
    file_out=os.path.join(output_dir,f_name)

    #creates new py file with the dict as a content
    with open(file_out,'w', encoding='utf-8') as f:
        dict_var = f_name.split('.')[0]
        f.write('{} = '.format(dict_var))
        f.write('{\n')
        #f.write(str(words_dict))
        for k,v in words_dict.items():
            f.write( '"' + k + '":' + str(v) + ',\n')
        f.write('}')
        print("file '{}' was saved in '{}'.".format(f_name,output_dir))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: make_dict word_file [output_dir]')
    if len(sys.argv) == 2:
        word_to_dictionary(sys.argv[1], None)
    else:
        word_to_dictionary(sys.argv[1], sys.argv[2])