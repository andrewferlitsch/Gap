""" Build Image Sample
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import os, sys, glob
import random 
import shutil

class img_utils:
    
    def __init__(self, main='./'):
        self.main = main
        self.labels = os.listdir(main)
        os.makedirs('{}_spl'.format(main), exist_ok=True)
        for lb in self.labels:
            os.makedirs('{}_spl/{}'.format(main, lb), exist_ok=True)
        self.labels_org = ['{}/{}'.format(main, lb) for lb in self.labels]
        self.labels_spl = ['{}_spl/{}'.format(main, lb) for lb in self.labels]

    def clean(self, source='org'):
        #clean sample folders
        if source == 'org':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please chose a source between "org" or "spl"')
        for lb in src_list:
            list_img = os.listdir(lb)
            for img in list_img:
                os.remove('{}/{}'.format(lb, img))

    def image_sample(self, spl=5, shufle=False):
        self.clean(source='spl')
        for lb in self.labels_org:
            list_img = os.listdir(lb)
            if random:
                #get a random image sample
                list_index = random.sample(range(0,len(list_img)), spl)
            else:
                #get the first images on folder
                list_index = list(range(0, spl))
            for index in list_index:
                org_file = '{}/{}'.format(lb, list_img[index])
                spl_file = '{}_spl/{}/{}'.format(self.main, lb.split('/')[-1], list_img[index])
                shutil.copy(org_file, spl_file)
            
    def img_rename(self, text=False, source='org'):
        if source == 'org':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please chose a source between "org" or "spl"')
        for lb in src_list:
            list_img = os.listdir(lb)
            for i, img in enumerate(list_img):
                dtype = img.split('.')[-1]
                if text:
                    os.rename('{}/{}'.format(lb, img), '{}/{}_{}.{}'.format(lb, text, i, dtype))
                else:
                    os.rename('{}/{}'.format(lb, img), '{}/{}.{}'.format(lb, i, dtype))
                    
    def img_replace(self, old=None, new=None, img_id=False, source='src'):
        if source == 'src':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please chose a source between "org" or "spl"')
        for lb in src_list:
            list_img = os.listdir(lb)
            for i, img in enumerate(list_img):
                if img_id:
                    os.rename('{}/{}'.format(lb,img),
                          '{}/{}'.format(lb, img.replace(old,'{}_{}'.format(new, i))))
                else:
                    os.rename('{}/{}'.format(lb, img),
                              '{}/{}'.format(lb, img.replace(old,new)))