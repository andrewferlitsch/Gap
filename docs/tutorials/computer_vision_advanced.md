# Computer Vision

## ADVANCED TOPICS

This section discusses more advanced topics in uses the **Gap** computer vision module.

### Processing Errors

The `Images` class tracks images that fail to be preprocessed. Examples for failure are: image does not exist, not an image, etc. The property `fail` will return the number of images that failed to preprocess and the property `errors` will return a list of tuples, where each tuple is the corresponding image argument that failed to preprocess, and the reason it failed.

```python
# assume that nonexist.jpg does not exist
images = Images(['good_image.jpg', 'nonexist.jpg'], 1)

# The length of the collection will be only one image (i.e., output from print is 1)
print(len(images))

# Will output 1 for the one failed image (i.e., nonexist.jpg)
print(images.fail)

# Will output: [ ('nonexist.jpg', 'FileNotFoundError') ]
print(images.errors)
```

### Image Dataset as Numpy Multi-Dimensional Array

Many of the machine learning frameworks come with prepared training sets for their tutorials, such as the MNIST, CIFAR, IRIS, etc. In some cases, the training set may already be in a numpy multi-dimensional format:

  *Color RGB*  
  Dimension 1: Number of Images  
  Dimension 2: Image Height  
  Dimension 3: Image Width  
  Dimension 4: Number of Channels  
  
  *Grayscale*  
  Dimension 1: Number of Images  
  Dimension 2: Image Height  
  Dimension 3: Image Width  
  
  *Flatten*  
  Dimension 1: Number of Images  
  Dimension 2: Flatten Pixel Data  
  
This format of a training set can be passed into the Images class as the `images` parameter. If the data type of the pixel data is `uint8` or `uint16`, the pixel data will be normalized; otherwise, data type is float, the pixel data is assumed to be already normalized.

```python
# Let's assume that the image data is already available in memory, such as being read in from file by openCV
import cv2
raw = []
raw.append(cv2.imread('image1.jpg'))  # assume shape is (100, 100, 3)
raw.append(cv2.imread('image2.jpg'))  # assume shape is (100, 100, 3)

# Let's assume now that the list of raw pixel images has been converted to a multi-dimensional numpy array
import numpy as np
dataset = np.asarray(raw)

print(dataset.shape)  # would print: (2, 100, 100, 3)

images = Images(dataset, labels)
print(len(images))      # will output 2
print(images[0].shape)  # will output (100, 100, 3)
```

### Image Dataset as Image Folder

In another case, a dataset is laid out as a set of subdirectories, each containing images, and where each subdirectory is a separate class. This directory/file layout is sometimes referred to as an Image Folder (e.g., Pytorch vision). Below is an example, where the classes are cat and dog:

```
dataset\
        cat\
            image1.jpg
            image2.jpg
            ...
        dog\
            image3.jpg
            image4.jpg
            ...
```

In this case, the root of the dataset (i.e., parent folder, e.g., dataset) is passed as the `images` parameter and the parameter `labels` is ignored. Each subdirectory (e.g., cat and dog) is a separate class name. In the above example, all the images under the subdirectories *cat* and *dog* are classified as a cat and dog, respectively. The `Images` object maps the class names (i.e., subdirectories) into integer labels, starting at zero. In the above example, cat *cat* is assigned the label 0 and *dog* is assigned the label 1.

```python
cats_and_dogs = Images('dataset', None)
print(cats_and_dogs[0].name, cats_and_dogs[0].label)
# Will output 'image1' and 0
```

The mapping of class names to integer labels is obtained from the property `classes` as a list of tuples, where each tuple is the class name, followed by the corresponding integer label.

```python
print(cats_and_dogs.classes)
# Will output: [ ('cat', 0), ('dog', 1) ]
```

### Reducing Storage by Deferring Normalization

In some cases, you may want to reduce your overall storage of the machine learning ready data. By default, each normalized pixel is stored as a float32, which consists of 4 bytes of storage. If the `config` setting `uint8` is specified, then normalization of the image is deferred. Instead, each pixel is kept unchanged (non-normalized) and stored as a uint8, which consists of a single byte of storage. For example, if a dataset of 200,000 images of shape (100,100,3) which has been normalized will require 24GB of storage. If stored unnormalized, the data will only require 1/4 the space, or 6GB of storage.

When the dataset is subsequently feed (i.e., properties `split`, `next()` and `minibatch`), the pixel data per image will be normalized in-place each time the image is feed.

```python
# Create the machine learning ready data without normalizing the image data
images = Images(dataset, labels, config=['uint8'])

# set 20% of the dataset as test and 80% as training
images.split = 0.2

# Run 100 epochs of the entire training set through the model
epochs = 100
for _ in range(epochs):
  # get the next image - which will be normalized in-place
  x, y = next(images)
  
  # send image through the neural network ....
```
