# Tutorials (Computer Vision)

## Introduction

Welcome to the labs.earth collaborative laboratory tutorials on machine learning. 

The computer vision (CV) tutorials will start with the basics and progress to advanced real world applications. The tutorials go beyond explaining the code and steps, to include the answers to the anticipated what and why questions.

Before the advent of machine learning with computer vision and today's modern ML/CV frameworks, working with and building real world applications was once the exclusive domain of imaging scientists. The <span style='color: saddlebrown'>Gap</span> framework extends modern computer vision to software developers, whom are familar with object oriented programming (OOP), object relational models (ORM), design patterns (e.g., MVC), asynchronous programming (AJAX), and microservice architectures.

For the data analyst and statisticians whom feel they don't have the necessary software development background, we encourage you to visit the collaborative lab's training site for fundamentials in modern software programming. Likewise, for those software developers whom feel they don't have the necessary background in statistics and machine learning, we encourage you to visit the collaborative lab's training site for fundamentials in [modern statistics and machine learning](https://github.com/andrewferlitsch/Training/tree/master/AITraining/Fundamentals/Machine%20Learning).

As far as our team and contributers, they keep a single phrase in mind when designing, coding and building tutorials. They like to say that Gap is:

                                            Machine Learning for Humans

## The First Steps in using Gap for Computer Vision (CV)

The first step in using Gap for machine learning (ML) of computer vision (CV) is learning to classify a single object in an image.
Is it a dog, a cat, what digit is it, what sign language digit is it, etc...

To do single object classification, depending on the images, one will use either a artificial neural network 
([ANN](https://github.com/andrewferlitsch/Training/blob/master/AITraining/Fundamentals/Machine%20Learning/ML%20Neural%20Networks.pptx)) 
or a convolutional neural network ([CNN](https://github.com/andrewferlitsch/Training/blob/master/AITraining/Fundamentals/Machine%20Learning/ML%20Convolutional%20Neural%20Networks.pptx)).

In either case, the raw pixel data is not directly inputted into a neural network. Instead, it has to be prepared into machine learning (ML) ready data. How it is prepared/transformed is dependent on the image source, the type and configuration of the
neural network, and the target application.

Images can come from a variety of sources, such as by your cell phone, images found on the Internet, a [facsimile image (FAX)](https://en.wikipedia.org/wiki/TIFF), a [video frame from a video stream](https://en.wikipedia.org/wiki/Film_frame#Video_frames), a [digitized medical/dental x-ray](https://en.wikipedia.org/wiki/Digital_radiography), a [magnetic resonance imaging (MRI)](https://en.wikipedia.org/wiki/Magnetic_resonance_imaging), a [electron microscopy (TEM)](https://en.wikipedia.org/wiki/Transmission_electron_microscopy), etc. 

Images go from very basic like [1-bit BW single channel (color plane)](https://en.wikipedia.org/wiki/Binary_image), to [8-bit gray scale single channel](https://en.wikipedia.org/wiki/Grayscale), to [8-bit color three channel (RGB)](https://en.wikipedia.org/wiki/8-bit_color), to [8-bit color four channel (+alpha channel)](https://en.wikipedia.org/wiki/Alpha_compositing), to [16-bit high tone (CMYK)](https://en.wikipedia.org/wiki/CMYK_color_model), to [infrared](https://en.wikipedia.org/wiki/Infrared_photography), to [stereoscopic images (3D)](https://en.wikipedia.org/wiki/Stereoscopy), [sound navigation and ranging (SONAR)](https://en.wikipedia.org/wiki/Sonar), to [RADAR](https://en.wikipedia.org/wiki/Radar), and more.

<img src="pixels.png">

<img src="color.png">

### Fundamentals in Preparing an Image for Machine Learning

Neural networks take as input numbers, specifically numbers that are continous real numbers and have been [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)). For images, pixel values are proportionally squashed between 0 and 1. For ANN networks, the inputs need to be a 1D vector, in which case the input data needs to be flatten, while in a CNN, the input is a 2D vector. Neural networks for computer vision take input of fixed sizes, so there is a transformation step to transform the pixel data to the input size and shape of the neural network, and finally assigning a label to the image (e.g., it's a cat). Again, for labels, neural networks use integer numbers; for example a cat must be assigned to a unique integer value and a dog to a different unique integer value. 

These are the basic steps for all computer vision based neural networks:

  - Transformation
  - Normalization
  - Shaping (e.g., flattening)
  - Labeling
  
 ### Importing Vision module
 
The <span style='color:saddlebrown'>Vision</span> module of the <span style='color: saddlebrown'>Gap</span> framework implements the classes and methods for computer vision. Within the [Vision](https://github.com/andrewferlitsch/Gap/blob/master/vision.py) module are two primary class objects for data management of images. The Image class manages individual images, while the Images class manages collections of images. As a first step, in your Python script or program you want to import from the Vision module the Image and Images class objects.

      from vision import Image, Images
 
 ### Preprocessing (Preparing) an image with Gap
  
Relative to the location of this tutorial are a number of test images used in verifying releases of Gap. For the purpose of these tutorials, the images that are part of the Gap release verification will be used for examples. The test file 1_100.jpg is a simple 100x100 96 dpi color image (RGB/8bit) from the Kaggle Fruit360 dataset. This dataset was part of a Kaggle contents to classify different types of fruits and their variety. It was a fairly simple dataset in that all the images were of the same size, type and number of channels. Further, each image contained only the object to classify (i.e., fruit) and was centered in the image.

The first step is to instantiate an Image class object and load the image into it, and its corresponding label. In the example below, an Image object is created where the first two positional parameters are the path to the image and the corresponding label (i.e., 1). 
  
      image = Image("../tests/files/1_100.jpg", 1)

While Python does not have OOP polymorphism builtin, the class objects in Gap have been constructed to emulate polymorphism in a variety of ways. The first positional parameter (image path) to the Image class can either be a local path or a remote path. In the latter case, a path starting with http or https is a remote path. In this case, a HTTP request to fetch the image from the remote location is made.

      image = Image("https://en.wikipedia.org/wiki/File:Example.jpg", 1)
      
Alternately, raw pixel data can be specified as the first (image) positional parameter, as a numpy array.

      raw = cv2.imread("../tests/files/1_100.jpg")
      image = Image(raw, 1)

Preprocessing of the image in the above examples is synchronous. The initializer (i.e., constructor) returns an image object once the image file has been preprocessed. Alternately, preprocessing of an image can be done asynchronously, where the preprocessing is performed by a background thread. Asynchronous processing occurs if the keyword parameter *ehandler* is specified. The value of the parameter is set to a function or method, which is invoked with the image object as a parameter when preprocessing of the image is complete.
  
      image = Image("../tests/files/1_100.jpg", 1, ehandler=myfunc)
      
      def myfunc(image):
        print("done")

The Image class has a number of attributes which are accessed using OOP properties (i.e., getters and setters). The attributes below provide information on the source image:

      print(image.name)   # the name of the image (e.g., 1_100)
      print(image.type)   # the type of the image (e.g., jpg)
      print(image.size)   # the size of the image in bytes (e.g., 3574)
      print(image.label)  # the label assigned to the image (e.g., 1)
      
The raw pixel data of the source image is accessed with the *raw* property, where property returns the uncompressed pixel data of the source image as a numpy array.

      raw = image.raw
      print(type(raw))    # outputs <class 'numpy.ndarry'>
      print(raw.shape)    # outputs the shape of the source image (e.g., (100, 100, 3))

The preprocessed machine learning ready data is accessed with the *data* property, where the property returns the data as a numpy array.

      data = image.data
      print(type(data))   # outputs <class 'numpy.ndarry'>
      print(data.shape)   # outputs the shape of the machine learning data (e.g., (100, 100, 3))
      
By default, the shape and number of channels of the source image are maintained in the preprocessed machine learning ready data, and the pixel values are normalized to values between 0 and 1. 

      print(raw[0][80])   # outputs pixel values (e.g., [250, 255, 255])
      print(data[0][80])  # outputs machine learning ready data values (e.g., [0.98039216, 1.0, 1.0])

When processing of the image is completed, the raw pixel data, machine learning ready data, and attributes are stored in a HDF5 (Hierarchical Data Format) formatted file. By default, the file is stored in the current local directory, where the rootname of the file is the rootname of the image. Storage provides the means to latter retrieval the machine learning ready data for feeding into a neural network, and/or retransforming the machine learning ready data. In the above example, the file would be stored as:

      ./1_100.hd5
      
The path location of the stored HDF5 can be specified with the keyword parameter *dir*.

      image = Image("../tests/files/1_100.jpg", 1, dir="tmp")
      
In the above example, the HDF5 file will be stored under the subdirectory *tmp*. If the subdirectory path does not exist, the Image object will attempt to create the folder.

The Image class optionally takes the keyword parameter *config*. This parameter takes a list of one or more settings, which alter how the image is preprocessed. For example, one can choose to use disable storing the HDF5 file using the keyword parameter *config* with the setting *nostore*.
    
      image = Image("../tests/files/1_100.jpg", 1, config=['nostore'])
      
### Example: Cloud-based Image Processing Pipeline

For a real-world example, let's assume one is developing a cloud based system that takes images uploaded from users, with the following requirements.

  - Handles multiple users uploading at the same time.
  - Preprocessing of the images is concurrent.
  - The machine learning ready data is passed to another step in a data (e.g., workflow) pipeline.
  
  Below is a bare-bones implementation.
  
      def first_step(uploaded_image, label):
        """ Preprocess an uploaded image w/label concurrently and then pass the preprocessed machine learning 
            ready data to another step in a data pipeline.
        """
        image = Image(uploaded_image, label, ehandler=next_step, config=['nostore'])
        
      def next_step(step):
        """ Do something with the Image object as the next step in the data pipeline """
        data = image.data
        
### Preprocessing Transformations: Resizing, Reshaping, Flattening

The keyword parameter *config* has a number of settings for specifying how the raw pixel data is preprocessed. The Gap framework is designed to eliminate the use of large numbers of keyword parameters, and instead uses a modern convention of passing in a configuration parameter. Here are some of the configuration settings:

        nostore                 # do not store in a HDF5 file
        grayscale | gray        # convert to a grayscale image with a single channel (i.e., color plane)
        flatten | flat          # flatten the machine learning ready data into a 1D vector
        resize=(height, width)  # resize the raw pixel data
        thumb=(height, width)   # create (and store) a thumbnail of the raw pixel data
        
Let's look how you can use these settings for something like neural network's equivalent of the hello world example ~ [training the MNIST dataset](https://www.tensorflow.org/versions/r1.0/get_started/mnist/beginners). The MNIST dataset consists of 28x28 grayscale images. Do to its size, grayscale and simplicity, it can be trained with just a ANN (vs. CNN). Since ANN take as input a 1D vector, the machine learning ready data would need to be reshaped (i.e., flatten) into a 1D vector.

        # An example of how one might use the Image object to preprocess an image from the MNIST dataset for a ANN
        image = Image("mnist_example.jpg", digit, config=["gray", "flatten"])
        
        print(image.shape)  # would output (784,)
        
In the above, the preprocessed machine learning ready data will be in a vector of size 784 (i.e., 28x28) with data type float. 

Let's look at another publicly accessible training set, the Fruits360 Kaggle competition. In this training set, the images are 100x100 RGB images (i.e., 3 channels). If one used a CNN for this training set, one would preserve the number of channels. But the input vector may be unneccessarily large for training purposes (30000 ~ 100x100x3). Let's reduce the size using the resize setting by 1/4.

        image = Image("../tests/files/1_100.jpg", config=['resize=(50,50)'])

        print(image.shape)  # would output (50, 50, 3)
        
### Example: Image Processing Dashboard

Let's expand on the real-word cloud example from earlier. In this case, let's assume that one wants to have a dashboard for a devOps person to monitor the preprocessing of images from a user, with the requirements:

  - Each time an image is preprocessed, the following is displayed on the dashboard:
    - A thumbnail of the source image.
    - The amount of time to preprocess the image.
    - Progress count of number of images preprocessed and accumulated time.
    
Here's the updated code:

      def first_step(uploaded_image, label):
        """ Preprocess an uploaded image w/label concurrently and then pass the preprocessed machine learning 
            ready data to another step in a data pipeline.
        """
        image = Image(uploaded_image, label, ehandler=second_step, config=['nostore', 'thumb=(16,16)'])
        
      nimages = 0
      nsecs   = 0
      
      def second_step(image):
        """ Display progress in dashboard """
        # Progress Accumulation
        nimages += 1
        nsecs += image.time
        
        # Construct message and pass thumbnail and msg to the dashboard
        msg = "Time %d, Number: %d, Accumulated: %f" % (time.time, nimages, nsecs)
        dashboard.display(img=image.thumb, text=msg)

        # The next processing step ...
        third_step(image)
        
Okay, there is still some problem with this example in that nimages and nsecs are global and would be trashed by concurrent processing of different users. The *ehandler* parameter can be passed a tuple instead of a single value. In this case, the Image object emulates polymorphism. When specified as a tuple, the first item in the tuple is the event handler and the remaining items are additional arguments to the event handler. Let's now solve the above problem by adding a new object *user* which is passed to the first function first_step(). The *user* object will have fields for accumulating the number of times an image was processed for the user and the accumulated time. The *ehandler* parameter is then modified to pass the *user* object to the event handler second_step().

      def first_step(uploaded_image, label, user):
        """ Preprocess an uploaded image w/label concurrently and then pass the preprocessed machine learning 
            ready data to another step in a data pipeline.
        """
        image = Image(uploaded_image, label, ehandler=(second_step, user), config=['nostore', 'thumb=(16,16)'])
      
      def second_step(image, user):
        """ Display progress in dashboard """
        # Progress Accumulation
        user.nimages += 1
        user.nsecs += image.time
        
        # Construct message and pass thumbnail and msg to the dashboard
        msg = "Time %d, Number: %d, Accumulated: %f" % (time.time, nimages, nsecs)
        dashboard.display(img=image.thumb, text=msg)

        # The next processing step ...
        third_step(image, user)
        
### Image Retrieval

By default, the Image class will store the generated HDF5 in the current working directory (i.e., ./). The keyword parameter *dir* tells the Image class where to store the generated HDF5 file.

        image = Image("../tests/files/1_100.jpg", dir='tmp')  # stored as tmp/1_100.h5

Once stored, the Image object subsequently can be retrieved (i.e., reused) from the HDF5 file. In the example below, an empty Image object is first instantiated, and then the method load() is invoked passing it the name (rootname) of the image and the directory where the HDF5 file is stored, if not in the current working directory.
        
        image = Image()
        image.load('1_100', dir='tmp')

        # retrieve the machine learning ready data from the loaded Image object
        data = image.data
        
### Image Reference

For a complete reference on all methods and properties for the Image class, see [reference](/specs/vision_spec.docx).

### Image Collections
   
The Images class provides preprocessing of a collections of images (vs. a single image). The parameters and emulated polymorphism are identical to the Image class, except the images and labels parameter refer to a plurality of images, which comprise the collection.



    
