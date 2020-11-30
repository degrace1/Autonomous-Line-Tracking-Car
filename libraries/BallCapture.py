from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
import math 
from imutils.video import VideoStream
from datetime import datetime
import os
'''given the fame (image of each capture)'''
class BallCapture:
    
    def __init__(self,yellowLower = (26,43,46), yellowUpper = (34,255,255), minR = 0, maxR = 80, vs = None):
        if vs == None:
            self.vs = VideoStream(src=0).start()
        else:
            self.vs = vs
        self.yellowLower = yellowLower
        self.yellowUpper = yellowUpper
        self.minR = minR
        self.maxR = maxR
        
    def coloredBallTracking(self):
        x = 0
        y = 0
        radius = 0
        # here is a small loop because some times the algorithm may fail to capture the colored in a frame, let ot 
        for i in range(3):
            # grab the current frame
            frame = self.vs.read()
            if frame is None:
                break
            # denoise with filter and convert it to the HSV soace
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            #mask teh yellow area and denoise with erode and dilation
            mask = cv2.inRange(hsv, self.yellowLower, self.yellowUpper)
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=3)

            # find contours 
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            
            #find the max connected part
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > self.minR and radius < self.maxR:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)
            key = cv2.waitKey(1) & 0xFF
            cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
            cv2.imwrite("mask//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',mask)
        return x,y,radius
    
    # compute the distance of a car given radius of the ball
    def dVision(self,radius):
        v = math.exp(-12.48963 * (1/radius))
        d = -8.974553 - (-2003.164/12.48963)*(1 - v)
        return d
    
    # capture the ball and compute the distance 
    def captureOne(self):
        # result = [x,y,radius]
        result = self.coloredBallTracking()
        print(result)
        # if result[2] (radius) == 0, then there is no ball detected
        if result[2] != 0:
            dis = self.dVision(result[2])
            print(dis)
            return result[0],result[1],result[2],dis
        else:
            return 0,0,0,-1
        
    #close the camera and all windows
    def endAll(self):
        self.vs.stop()
        cv2.destroyAllWindows() 