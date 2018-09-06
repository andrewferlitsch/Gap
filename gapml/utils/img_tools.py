""" Image Utils
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import os, sys
import random 
import shutil

class img_utils:
    """ image utils """

    def __init__(self, main='./'):
        self.main   = main             #data folder where labels are located
        self.labels = os.listdir(main) #list of images labels

        #creates sample directory
        os.makedirs('{}_spl'.format(main), exist_ok=True)

        #creates labels folders into the sample directory 
        for lb in self.labels:
            os.makedirs('{}_spl/{}'.format(main, lb), exist_ok=True)

        #list of labels into main folder
        self.labels_org = ['{}/{}'.format(main, lb) for lb in self.labels]

        #list of labels into sample folder
        self.labels_spl = ['{}_spl/{}'.format(main, lb) for lb in self.labels]

    def clean(self, source='org'):
        """
        clean label folders
        :param source: give the option of folder to clean
                       between folder origin "org" or sample "spl"
        """

        #verify which folder will be cleaned
        if source == 'org':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please choose a source between "org" or "spl"')

        #remove images from each label
        for lb in src_list:
            list_img = os.listdir(lb)
            for img in list_img:
                os.remove('{}/{}'.format(lb, img))

    def img_sample(self, spl=5, shufle=False):
        """
        Images Sample
        :param spl:    give the number of pictures for label
        :param shufle: select ramdom images per label or the first on the list
        """
        #clean labels
        self.clean(source='spl')

        for lb in self.labels_org:
            #list of images per label
            list_img = os.listdir(lb)
            if random:
                #get a random image sample
                list_index = random.sample(range(0,len(list_img)), spl)
            else:
                #get the first images on folder
                list_index = list(range(0, spl))
            #copy selected images into sample labels
            for index in list_index:
                org_file = '{}/{}'.format(lb, list_img[index])
                spl_file = '{}_spl/{}/{}'.format(self.main, lb.split('/')[-1], list_img[index])
                shutil.copy(org_file, spl_file)
            
    def img_rename(self, text=None, source='org'):
        """
        Rename Images
        :param text:   give a text for your images name
        :param source: give the option of folder to rename
                       between folder origin "org" or sample "spl"
        """

        #verify which folder will be renamed
        if source == 'org':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please chose a source between "org" or "spl"')
        for lb in src_list:
            list_img = os.listdir(lb)
            #list of images per label
            for i, img in enumerate(list_img):
                dtype = img.split('.')[-1]
                if text != None:
                    os.rename('{}/{}'.format(lb, img), '{}/{}_{}.{}'.format(lb, text, i, dtype))
                else:
                    os.rename('{}/{}'.format(lb, img), '{}/{}.{}'.format(lb, i, dtype))
                    
    def img_replace(self, old=None, new=None, img_id=False, source='src'):
        """
        Rename Images
        :param old:    
        :param new:    
        :param img_id: 
        :param source: give the option of folder to rename
                       between folder origin "org" or sample "spl"
        """
        if source == 'src':
            src_list = self.labels_org
        elif source == 'spl':
            src_list = self.labels_spl
        else:
            print('please chose a source between "org" or "spl"')
        for lb in src_list:
            list_img = os.listdir(lb)
            #list of images per label
            for i, img in enumerate(list_img):
                if img_id:
                    os.rename('{}/{}'.format(lb,img),
                          '{}/{}'.format(lb, img.replace(old,'{}_{}'.format(new, i))))
                else:
                    os.rename('{}/{}'.format(lb, img),
                              '{}/{}'.format(lb, img.replace(old,new)))