""" Image Utils
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

import os
import sys
import random
import shutil

class img_utils:
    """
    Type of Folder Tree

    ## tree = 1 ##
    [root_path] "folder_name"/..
        [subfolder] class_0/..
        [subfolder] class_1/..
        [subfolder] errors/..

    ## tree = 2 ##
    [root_path] "folder_name"/..
        [subfolder] train_tr/..
            [subfolder] class_0/..
            [subfolder] class_1/..
        [subfolder] train_val/..
            [subfolder] class_0/..
            [subfolder] class_1/..
        [subfolder] test/test/..
        [subfolder] errors/..
    """

    def __init__(self, root_path='./', tree=1, transf='1to2', rm=False):
        """Make directories"""
        self.labels = os.listdir(root_path)      # list of images labels
        self.root_path = root_path.split('/')[0] # root folder where labels are located
        self.tree = tree                         # folder structure to the end sample
        self.transf = transf                     # type of folder tree to tranform '1to2' or '2to1'
        self.rm = rm                             # warning! remove folder from directory
        
        if rm:
            answere_ok = False
            while answere_ok == False:
                try:
                    warning = input('Warning! this will delete your image dataset. Are you sure? [Yes/no]: ')
                    warning = warning[0].lower()
                    if warning == 'y' or warning == 'n':
                        answere_ok = True
                except:
                    continue
            if warning == 'y':
                shutil.rmtree(self.root_path)
                print('Your files were deleted!')
        
    def _list_labels_org(self):
        # list of labels into root_path folder
        if self.transf == '1to2':
            self.labels_org = ['{}/{}'.format(self.root_path, lb) for lb in self.labels]
        elif self.transf == '2to1':
            self.root_path = self.root_path[:-3]
            train_tr = ['{}_t2/train_tr/{}'.format(self.root_path, lb) for lb in self.labels]
            train_val = ['{}_t2/train_val/{}'.format(self.root_path, lb) for lb in self.labels]
            self.labels_org = train_tr + train_val
    
    def _src_list(self):
        # list of labels for folders that will be renamed
        if self.tree == 1:
            self.src_list = ['{}/{}'.format(self.root_path, lb) for lb in self.labels]
        if self.tree == 2:
            train_tr = ['{}/train_tr/{}'.format(self.root_path, lb) for lb in self.labels]
            train_val = ['{}/train_val/{}'.format(self.root_path, lb) for lb in self.labels]
            self.src_list = train_tr + train_val
            
    def _makedirs(self):
        """ Make Directories"""
        #creates folders structure
        if self.tree == 1:
            for lb in self.labels:
                os.makedirs('{}{}/{}'.format(self.root_path, self.end, lb), exist_ok=True)
        elif self.tree == 2:
            for lb in self.labels:
                os.makedirs('{}{}/train_tr/{}'.format(self.root_path, self.end2, lb), exist_ok=True)
                os.makedirs('{}{}/train_val/{}'.format(self.root_path, self.end2, lb), exist_ok=True)
            os.makedirs('{}{}/test/test'.format(self.root_path, self.end2), exist_ok=True)
            os.makedirs('{}{}/errors'.format(self.root_path, self.end2), exist_ok=True)
        elif self.tree == None:
            pass
        else:
            print('select between tree=1 or tree=2')

    def _copy_move(self, ppath, action, lb, list_img, index):
        """
        Copy or Move images
        :param ppath:     Required. Partial path
        :param action:    Required. Select between 'copy' or 'move'
        :param lb:        Required. Label name
        :param list_img:  Required. List of images per class
        :param index:     Required. Index image in the list
        """
        # verify type of tree to transform
        if self.transf == '1to2':
            org_file = '{}/{}'.format(lb, list_img[index])
            dst_file = '{}{}/{}/{}'.format(self.root_path, ppath, lb.split('/')[-1], list_img[index])
        elif self.transf == '2to1':
            org_file = '{}/{}'.format(lb, list_img)
            dst_file = '{}/{}/{}'.format(self.root_path, lb.split('/')[-1], list_img)
        
        # move or copy images into new tree structure
        if action == 'copy':
            shutil.copy(org_file, dst_file)
        elif action == 'move':
            shutil.move(org_file, dst_file)
        else:
            print('select copy or move')
            
    def img_container(self, action='copy', spl=5, shufle=False, img_split=0.2):
        """
        Images Container
        :param action:    Select between 'copy' or 'move'
        :param spl:       Select the number of pictures for label to create the sample
        :param shufle:    select ramdom images per label or the first images on the list
        :param img_split: percentage of split between train / val
        """
        
        # specifies the name for the root_path
        if action == 'copy':
            self.end  = '_spl'
            self.end2 = '_t2' + self.end
        elif action == 'move':
            self.end  = ''
            self.end2 = '_t2'
        else:
            print('select copy or move')
        
        # creates list of labels from root_path
        self._list_labels_org()
            
        # creates the directories
        self._makedirs()
        
        for lb in self.labels_org:
            # list of images per label
            list_img = os.listdir(lb)
            # total of images per class 
            len_list_img = len(list_img)
            
            # sets a sample number or total of images per class to move or copy 
            if action == 'copy':
                spl = spl
            elif action == 'move':
                spl = len_list_img
            else:
                print('select copy or move')
            
            if shufle:
                #get a random image sample
                list_index = random.sample(range(len_list_img), spl)
            else:
                #get the first images on folder
                list_index = list(range(spl))
            
            # move images from tree 2 to tree 1
            if self.transf == '2to1':
                for img in list_img:
                    ppath = None
                    action = 'move'
                    index = None
                    self._copy_move(ppath, action, lb, img, index)
                self.tree = None
            
            # copy or move selected images into the sample labels depending of the selected tree
            if self.tree == 1:
                for index in list_index:
                    self._copy_move('_spl', action, lb, list_img, index)
          
            elif self.tree == 2:
                img_tr = int(len(list_index) * (1 - img_split))
                count = 0
                for index in list_index:
                    if count <= img_tr:
                        # move or copy images in the train folder
                        self._copy_move('{}/train_tr'.format(self.end2), action, lb, list_img, index)
                    else:
                        # move or copy images in the validation folder
                        self._copy_move('{}/train_val'.format(self.end2), action, lb, list_img, index)
                    count += 1
            elif self.tree == None:
                pass
            else:
                print('select 1 or 2')
                
    def transform(self, shufle=False, img_split=0.2):
        """
        Transform
        :param shufle:    select ramdom images per label or the first images on the list
        :param img_split: percentage of split between train / val
        """
        # move the files between tree structures
        action = 'move'
        if self.transf == '1to2':
            self.tree = 2
            spl = None
            self.img_container(action, spl, shufle, img_split)
            shutil.rmtree(self.root_path)
        elif self.transf == '2to1':
            self.img_container(action)
            shutil.rmtree('{}_t2'.format(self.root_path))
        else:
            print('select 1to2 or 2to1')
            
    def img_rename(self, text=None):
        """
        Rename Images
        :param text:   give a text for your images name
        """
        
        # creates source list
        self._src_list()
                
        for lb in self.src_list:
            # list of images per label
            list_img = os.listdir(lb)
            # extract label name
            text_lb = lb.split('/')[-1]
            for i, img in enumerate(list_img):
                dtype = img.split('.')[-1]
                if text == True:
                    os.rename('{}/{}'.format(lb, img), '{}/{}_{}.{}'.format(lb, text_lb, i, dtype))
                elif text != None:
                    os.rename('{}/{}'.format(lb, img), '{}/{}_{}.{}'.format(lb, text, i, dtype))
                else:
                    os.rename('{}/{}'.format(lb, img), '{}/{}.{}'.format(lb, i, dtype))
                    
    def img_replace(self, old, new, img_id=False):
        """
        Rename Images
        :param old:    Required. The text you want to replace.
        :param new:    Required. The text you want to replace "old" with.
        :param img_id: True to enumerate by id name_id
        """
        # creates source list
        self._src_list()
        
        for lb in self.src_list:
            # list of images per label
            list_img = os.listdir(lb)
            for i, img in enumerate(list_img):
                if img_id:
                    os.rename('{}/{}'.format(lb, img),
                              '{}/{}'.format(lb, img.replace(old,'{}_{}'.format(new, i))))
                else:
                    os.rename('{}/{}'.format(lb, img),
                              '{}/{}'.format(lb, img.replace(old,new)))
