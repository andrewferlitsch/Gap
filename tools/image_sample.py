""" Build Image Sample
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import os, sys
import random 
import shutil

def image_sample(main, sample):
    labels = os.listdir(main)
    os.makedirs('{}_spl'.format(main), exist_ok=True)

    for lb in labels:
        os.makedirs('{}_spl/{}'.format(main,lb), exist_ok=True)

    labels_src = ['{}/{}'.format(main,lb) for lb in labels]
    labels_dst = ['{}_spl/{}'.format(main,lb) for lb in labels]

    #clean sample folders
    for lb in labels_dst:
        for f in glob.glob(lb):
            os.remove(f)

    for lb in labels_src:
        list_tr = os.listdir(lb)
        list_index = random.sample(range(0,len(list_tr)),sample)
        for index in list_index:
            src_file = os.path.join(lb, list_tr[index])
            dst_file = os.path.join('{}_spl/{}'.format(main,lb.split('/')[-1]), list_tr[index])
            shutil.copy(src_file, dst_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: image_sample image_path sample')
    if len(sys.argv) == 2:
        image_sample(sys.argv[1],sys.argv[1])
        