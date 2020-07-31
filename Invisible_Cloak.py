import cv2 as CV
import numpy as NP
import time

print("A Magic Trick. \nTry this and you will be able to make yourself invisible and shock your friends. \nGet ready to try it...!")
#read the readme.md file for detailed explanation
#Creating an VideoCapture object
cam=CV.VideoCapture(0)
#just to make your camera warmup!!! 
time.sleep(3)
#initializing background variable
background=0

for i in range(60):
    ret,background=cam.read()

while(cam.isOpened()):
    
    #start reading the image from camera
    ret,image=cam.read()

    #inverse the captured image
    #image=NP.flip(image,axis=1)

    #convert BGR to HSV color space values
    HSV=CV.cvtColor(image,CV.COLOR_BGR2HSV)
    value=(35,35)

    blur_parts=CV.GaussianBlur(HSV,value,0)

    #red color masking
    #range 1
    lower=NP.array([0,120,70])
    upper=NP.array([10,255,255])
    mask1=CV.inRange(HSV,lower,upper)
    
    #range 2
    lower=NP.array([170,120,70])
    upper=NP.array([180,255,255])
    mask2=CV.inRange(HSV,lower,upper)

    #addition of the above two mask to get final mask block
    mask=mask1+mask2

    mask=CV.morphologyEx(mask,CV.MORPH_OPEN,NP.ones((5,5),NP.uint8))

    #replacing pixels of the cloth with background pixels
    image[NP.where(mask==255)]=background[NP.where(mask==255)]
    CV.imshow("Show",image)
    wait_time=CV.waitKey(10)
    if wait_time==27:
        break
    
    
