# Tutorials (Computer Vision)

## Introduction

Welcome to the labs.earth collaborative laboratory tutorials on machine learning. 

The computer vision (CV) tutorials will start with the basics and progress to advanced real world applications. The tutorials go beyond explaining the code and steps, to include the answers to the anticipated what and why questions.

Before the advent of machine learning with computer vision and today's modern ML/CV frameworks, working with and building real world applications was once the exclusive domain of imaging scientists. The <span style='color: saddlebrown'>Gap</span> framework extends modern computer vision to software developers, whom are familar with object oriented programming (OOP), object relational models (ORM), design patterns (e.g., MVC), asynchronous programming (AJAX), and microservice architectures.

For the data analyst and statisticians whom feel they don't have the necessary software development background, we encourage you to visit the collaborative lab's training site for fundamentials in modern software programming. Likewise, for those software developers whom feel they don't have the necessary background in statistics and machine learning, we encourage you to visit the collaborative lab's training site for fundamentials in [modern statistics and machine learning](https://github.com/andrewferlitsch/Training/tree/master/AITraining/Fundamentals/Machine%20Learning).

As far as our team and contributers, they keep a single phrase in mind when designing, coding and building tutorials. They like to say that Gap is:

                                             *Machine Learning for Humans*

## The First Steps in using Gap for Computer Vision (CV)

The first step in using Gap for machine learning (ML) of computer vision (CV) is learning to classify a single object in an image.
Is it a dog, a cat, what digit is it, what sign language digit is it, etc...

To do single object classification, depending on the images, one will use either a artificial neural network 
([ANN](https://github.com/andrewferlitsch/Training/blob/master/AITraining/Fundamentals/Machine%20Learning/ML%20Neural%20Networks.pptx)) 
or a convolutional neural network ([CNN](https://github.com/andrewferlitsch/Training/blob/master/AITraining/Fundamentals/Machine%20Learning/ML%20Convolutional%20Neural%20Networks.pptx)).

In either case, the raw pixel data is not directly inputted into a neural network. Instead, it has to be prepared into machine learning (ML) ready data. How it is prepared/transformed is dependent on the image source, the type and configuration of the
neural network, and the target application.

Images can come from a variety of sources, such as by your cell phone, images found on the Internet, [facsimile image (FAX)](https://en.wikipedia.org/wiki/TIFF), [video frame from a video stream](https://en.wikipedia.org/wiki/Film_frame#Video_frames), [digitized medical/dental x-ray](https://en.wikipedia.org/wiki/Digital_radiography), [magnetic resonance imaging (MRI)](https://en.wikipedia.org/wiki/Magnetic_resonance_imaging), [electron microscopy (TEM)](https://en.wikipedia.org/wiki/Transmission_electron_microscopy), etc. 

Images go from very basic like [1-bit BW single channel (color plane)](https://en.wikipedia.org/wiki/Binary_image), to [8-bit gray scale single channel](https://en.wikipedia.org/wiki/Grayscale), to [8-bit color three channel (RGB)](https://en.wikipedia.org/wiki/8-bit_color), to [8-bit color four channel (+alpha channel)](https://en.wikipedia.org/wiki/Alpha_compositing), to [16-bit high tone (CMYK)](https://en.wikipedia.org/wiki/CMYK_color_model), to [infrared](https://en.wikipedia.org/wiki/Infrared_photography), to [stereoscopic images (3D)](https://en.wikipedia.org/wiki/Stereoscopy), [sound navigation and ranging (SONAR)](https://en.wikipedia.org/wiki/Sonar), to [RADAR](https://en.wikipedia.org/wiki/Radar), and more.

### Fundamentals in Preparing an Image for Machine Learning

Neural networks take as input numbers, specifically numbers that are continous real numbers and have been [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)). For images, pixel values are proportionally squashed between 0 and 1. For ANN networks, the inputs need to be a 1D vector, in which case the input data needs to be flatten, while in a CNN, the input is a 2D vector. Neural networks for computer vision take input of fixed sizes, so there is a transformation step to transform the pixel data to the input size and shape of the neural network, and finally assigning a label to the image (e.g., it's a cat). Again, for labels, neural networks use integer numbers; for example a cat must be assigned to a unique integer value and a dog to a different unique integer value. 

These are the basic steps for all computer vision based neural networks:

  - Transformation
  - Normalization
  - Shaping (e.g., flattening)
  - Labeling
  
 ### Importing Vision module
 
The <span style='color:saddlebrown'>Vision</span> module of the <span style='color: saddlebrown'>Gap</span> framework implements the classes and methods for computer vision. 

      from vision import Image, Images
 
 ### Preparing an image with Gap
  
Relative to the location of this tutorial are a number of test images used in verifying releases of Gap. For the purpose of then tutorials, the images that are part of the Gap release verification will be used for examples.
  
      image = Image("../files/1_100.jpg", 1)
