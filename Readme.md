# Invisibility Cloak Python
This explanation explains key concepts of `image processing` using `opencv` with python.
I will try my best to explain [code](Invisibile_Cloak.py)

# Installation     

Clone this repo to your local machine: `git clone https://github.com/Ashutosh-Srivastava/Invisible-Cloak`    

### Importing all the required libraries
```python
import cv2 as CV
import numpy as NP
import time
```

### Capturing the static background frame
In order to replace the current frame pixels with the background pixels for invisibility
effect we need to store the frame of a static background FIRST.

```python
#Creating an VideoCapture object
cam=CV.VideoCapture(0)
#just to make your camera warmup!!! 
time.sleep(3)
#initializing background variable
background=0

for i in range(60):
    ret,background=cam.read()
```

If you wish to use this with your web cam, change line 8 to `cam = CV.VideoCapture(0)`
or if you wish to use it with a pre-recorded video, change it to `cam = CV.VideoCapture(r"video_path")` 
and enter your video path in double quotes for ex. `cam = CV.VideoCapture(r"C:\Users\Dell\Documents\test.mp4")`.

>cam.read() method enables us to capture latest frame(stored in variable `background`) with the camera
>and it also returns a Boolean (True/False stored in `ret`). If frame is read correctly, it will be True else False.
>So you can check end of the video by checking this return value.

###### Why capture background image using a for loop ?
As the background is static we can do with a single capture right ?
Yes, but the image captured is dark as compared to when we capture multiple frames are captured. 
Therefore capturing multiple images of static background with a for loop.

### Understanding the while loop
`cam.isOpened()` Returns true if cap is initialized.
Just like we got the frames for background we try to recieve 
current frames in the while loop using `ret, image = cap.read()`

#### Extracting red color in the image.
So the idea is that we will use a red color cloth as out invisibility cloak.
We will first determine the region covered by the cloth (`determine pixels corresponding to red color`).
To detect red color we use the HSV color space. 

We convert the image into HSV color space using the following line of code.
```python
#convert BGR to HSV color space values
HSV=CV.cvtColor(image,CV.COLOR_BGR2HSV)
```
Using HSV(Hue-Saturation-Value) color space we can distinguish 
between different colors much accurately than we can in RGB color space.

###### Setting range of HSV values for red color detection
Below code is used to detect pixels corresponding to the red color cloth.
```python
#red color masking
    #range 1
    lower=NP.array([0,120,70])
    upper=NP.array([10,255,255])
    mask1=CV.inRange(HSV,lower,upper)
    
    #range 2
    lower=NP.array([170,120,70])
    upper=NP.array([180,255,255])
    mask2=CV.inRange(HSV,lower,upper)
```
Hue range | 0-10 | 170-180
---|---|---

>The Hue values actually range between 0-360 degrees but
>in OpenCV to fit into 8bit value the range is from 0-180.
>Red color is represented by 0-10 and 170-180 values.


Saturation range | 120-255
---|---
> Saturation represents purity of color. Pure Red, Green and Blue
>are considered to be true saturated colors. As saturation decreases the effect of the other two
>color component increases.
> Here we set the above value because our cloth is of highly saturated red color.

Value range | 70-255
---|---
> Value corresponds to the brightness of the image. For a given pixel if the value is increased or 
> decreased then values of R,G and B will increase or decrease respectively but their percentage 
>contribution will remain unchanged.
> The lower value of the range is 70 so that we can detect red color in the wrinkles of the cloth as well.

The below command returns an array with pixel value = 255  for pixels 
having HSV values within upper and lower value range and 0 otherwise.
This way we generate a mask.
```python
mask=CV.morphologyEx(mask,CV.MORPH_OPEN,NP.ones((5,5),NP.uint8))
```

And finally we `OR` both the masks (mask0 and mask1) to get 
our final mask. 
```python
mask=mask1+mask2
```
This is also a simple example of operator overloading of `+`.

`mask=CV.morphologyEx(mask,CV.MORPH_OPEN,NP.ones((5,5),NP.uint8))` This line of code
removes small regions of false detection which will avoid random glitches in the final output.

##### Here's the trick !!
`image[NP.where(mask==255)]=background[NP.where(mask==255)]`
What we do in this line is quite simple. We access all the pixels which have value of 255 
in the final mask (`The pixels corresponding to the detected red color`), and we replace the pixel values 
with the pixel values of respective coordinates in the background frame. That's the trick. 



