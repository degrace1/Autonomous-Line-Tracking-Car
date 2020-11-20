from BallCapture import *
from ExampleCamera import *
from DistanceCamera import *
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
# HSV threshold, we use the yellow color ball here 
yellowLower = (26,43,46)
yellowUpper = (34,255,255)

vs = VideoStream(src=0).start()
   
# allow the camera or video file to warm up
time.sleep(2.0)

for i in range(1000):
    frame = vs.read()
    result = coloredBallTracking(frame)
    print(result)
# open the camera
cv2.destroyAllWindows() 
vs.stop() 

# allow the camera or video file to warm up



# close all windows
#cv2.destroyAllWindows()