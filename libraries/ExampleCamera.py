from BallCapture import *
from ExampleCamera import *
from DistanceCamera import *
from imutils.video import VideoStream
import cv2
import imutils

# HSV threshold, we use the yellow color ball here 
yellowLower = (26,43,46)
yellowUpper = (34,255,255)

#initilize a ball capture class
c = BallCapture()

time.sleep(2.0)
for i in range(1000):
    #get the information of each frame
    print(c.captureOne())

#end the program
c.endAll()
#close the camera and all windows

 
