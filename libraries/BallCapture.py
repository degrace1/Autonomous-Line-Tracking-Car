from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
from imutils.video import VideoStream

'''given the fame (image of each capture)'''
def coloredBallTracking(vs, yellowLower = (26,43,46), yellowUpper = (34,255,255), minR = 0, maxR = 80):
        x = 0
        y = 0
        radius = 0
        # here is a small loop because some times the algorithm may fail to capture the colored in a frame, let ot 
        for i in range(3):
            # grab the current frame
            frame = vs.read()
            if frame is None:
                break
            # denoise with filter and convert it to the HSV soace
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            #mask teh yellow area and denoise with erode and dilation
            mask = cv2.inRange(hsv, yellowLower, yellowUpper)
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
                if radius > minR and radius < maxR:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)
            key = cv2.waitKey(1) & 0xFF
            cv2.imwrite('p'+str(i)+'.jpg',frame)
        
        return x,y,radius
