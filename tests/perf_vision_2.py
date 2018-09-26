from gapml.vision import Image, Images
from PIL import Image as PILImage
import cv2
import h5py
import sys
import os
import time
import numpy as np

print("TEST W/O FLATTENING")

# Gap
#
labels = ['flower_photos/daisy']
start = time.time()
images = Images(labels, list(range(len(labels))), config=['resize=(224,244)', 'uint8'], name='flower')
print("GAP", time.time() - start, "secs")

st = os.stat('flower.h5')
print(st.st_size // (1024*1024), "MB, No. Images ", len(images), " Shape ", images[0].shape, " Type ", type(images[0].data[0][0][0]))
images = None
os.remove('flower.h5')

root_path = 'flower_photos'
labels = ['daisy']

# Hardcoded
def hardcoded(labels):
    imgdata = []
    classes = []
    for i, lb in enumerate(labels):
        #list of images per label origen
        list_img = os.listdir(lb)
        for img in list_img:
            image = PILImage.open('{}/{}'.format(lb, img))
            image = np.array(image)
            image = cv2.resize(image, (224,224))
            imgdata.append(image)
            classes.append(i)
    return imgdata, classes
    
train_tr  = ['{}/{}'.format(root_path, lb) for lb in labels]

start = time.time()

images, classes_tr = hardcoded(train_tr)

# Write the images and labels to disk as HD5 file
with h5py.File('flower.h5', 'w') as hf:
    hf.create_dataset("imgdata", data=images)
    hf.create_dataset("classes", data=classes_tr)

print("CV2", time.time() - start, "secs")

st = os.stat('flower.h5')
print(st.st_size // (1024*1024), "MB, No. Images ", len(images), " Shape ", images[0].shape, " Type ", type(images[0][0][0][0]))
images = None
os.remove('flower.h5')

print("TEST WITH FLATTENING")

# Gap
#
labels = ['flower_photos/daisy']
start = time.time()
images = Images(labels, list(range(len(labels))), config=['resize=(224,244)'], name='flower')
print("GAP", time.time() - start, "secs")

st = os.stat('flower.h5')
print(st.st_size // (1024*1024), "MB, No. Images ", len(images), " Shape ", images[0].shape, " Type ", type(images[0].data[0][0][0]))
images = None
os.remove('flower.h5')

# Hardcoded
#
root_path = 'flower_photos'
labels = ['daisy']

def hardcoded2(labels):
    imgdata = []
    classes = []
    for i, lb in enumerate(labels):
        #list of images per label origen
        list_img = os.listdir(lb)
        for img in list_img:
            image = PILImage.open('{}/{}'.format(lb, img))
            image = np.array(image)
            image = cv2.resize(image, (224,224))
            image = (image / 255.0).astype(np.float32)
            imgdata.append(image)
            classes.append(i)
    return imgdata, classes
    
train_tr  = ['{}/{}'.format(root_path, lb) for lb in labels]

start = time.time()

images, classes_tr = hardcoded2(train_tr)

# Write the images and labels to disk as HD5 file
with h5py.File('flower.h5', 'w') as hf:
    hf.create_dataset("imgdata", data=images)
    hf.create_dataset("classes", data=classes_tr)

print("CV2", time.time() - start, "secs")

st = os.stat('flower.h5')
print(st.st_size // (1024*1024), "MB, No. Images ", len(images), " Shape ", images[0].shape, " Type ", type(images[0][0][0][0]))
images = None
os.remove('flower.h5')