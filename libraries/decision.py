# Decision
# This class determines how a car will run and avoid obstacles in its
# path based on its priority level.

import time
from Motor import *
from Line_Tracking import *
from slow import Slow_Tracking
from network.client.src.NetworkPackage import *
from BallCapture import *
import cv2
import os
import shutil


class Decision:
    # Constructor
    def __init__(self, id):
        self.car = CarState(id,0,0,0,0,0,0) # Initialize car state object
        self.line = Line_Tracking() # Car line follower algorithm
        self.time = time.time()
        self.vs = VideoStream(src=0).start()
        self.BallTrack = BallCapture(vs = self.vs) # Initialize object detection class
        
        dir = 'frame' # Directory for captured images
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        
        self.label = (10,30) # Text label for images

    # Run
    # This method calls the appropiate method based on the priority level of the car. It
    # will continue running until control C is pressed.
    def run(self):
        try:
            if self.car.getID() == 0: # Car only traces line
                print('This car has high priority.')
                self.highPriority()
                
            elif self.car.getID() == 1: # Car stops for one car or 5s
                print('This car has medium priority.')
                self.mediumPriority()
                
            else: # Car stops until no cars are in view
                print('This car has low priority.')
                self.lowPriority()
                
        except KeyboardInterrupt: 
            PWM.setMotorModel(0, 0, 0, 0) # Car stops once control C pressed

    # High Priority
    # Car has ID 0 and has the highest priority to the track. This car will follow
    # the line with no interruptions. 
    def highPriority(self):
        print("This car has priority on the track over every other car. Keep running!")
        while True:
            frame = self.vs.read()
            cv2.putText(frame, text='High Priority Car', org=self.label,
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
            thickness=2, lineType=cv2.LINE_AA)
            cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
            self.line.run()

    # Medium Priority
    # Car has ID 1 and has the second highest priority to the track. This car will
    # follow the line. If the ultrasonic sensor detects an object within 30 cm, the
    # car will slow down until the car is at least 50 cm away. If the camera detects
    # an object, the car will stop until the object is out of view or until 5 s has elapsed.
    def mediumPriority(self):
        slow = Slow_Tracking()
        while True:
            if self.car.getUltrasonic() < 20: # Ultrasonic sensor detects an object that is close
                print("There is an object within 20 cm of the car, slow down!")
                start = time.time()
                update = time.time()
                while self.car.getUltrasonic() < 25  and update - start < 5:
                    print("There is an object ", self.car.getUltrasonic(), " cm away from the car.")
                    frame = self.vs.read()
                    cv2.putText(frame, text="There is an object close by.", org=self.label,
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text="Distance: " + str(self.car.getUltrasonic()), org=(self.label[0],self.label[1]+30),
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                    cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                    slow.run()
                    
            elif self.BallTrack.captureOne()[3] < 20 : # Camera detects an object that is close
                slow = Slow_Tracking()
                PWM.setMotorModel(0, 0, 0, 0)
                print("There is an object within 30 cm of the car, slow down!")
                start = time.time()
                update = time.time()
                while (self.BallTrack.captureOne()[3] < 25 ) and update - start < 5: # While camera sees something to the side or 5 s has not elapsed
                    print("There is an object ", self.BallTrack.captureOne()[3], " cm away from the car.")
                    PWM.setMotorModel(0, 0, 0, 0)
                    update = time.time()
                    
            else: # Nothing in the way, run normally
                frame = self.vs.read()
                cv2.putText(frame, text="No objects are detected.", org=self.label,
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                print("nothing find keep running!")
                self.line.run()

    # Low Priority
    # Car has ID 2 and has the third highest priority to the track. This car will follow
    # the line. If the ultrasonic sensor detects an object within 30 cm, the car will stop
    # until it's at least 50 cm away. If the camera de
    def lowPriority(self):
        while True:
            self.car.setUltrasonic() 
            print(self.car.getUltrasonic())
            if self.car.getUltrasonic() < 30: # Ultrasnoic sensor detects that an object is close
                print("ultrasonic finds an object near!","distance = ", self.car.getUltrasonic())
                while self.car.getUltrasonic() < 40:
                    self.car.setUltrasonic() 
                    PWM.setMotorModel(0, 0, 0, 0) # Stop
                    print("There is an object ", self.car.getUltrasonic(), " cm away.")
                    frame = self.vs.read()
                    cv2.putText(frame, text="There is an object close by", org=self.label,
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text="Distance: "+ str(self.car.getUltrasonic()), org=(self.label[0],self.label[1]+30),
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                    cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                    
            elif self.BallTrack.captureOne()[3] < 30: # Camera detects that an object is close
                PWM.setMotorModel(0, 0, 0, 0)
                print("camera finds an object near!")
                while self.BallTrack.captureOne()[3] < 40:
                    print("the object is still close!")
                    PWM.setMotorModel(0, 0, 0, 0)
                    
            else: # Nothing in the way, run normally
                print("No objects are detected. ")
                frame = self.vs.read()
                cv2.putText(frame, text="No objects are detected.", org = self.label,
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255),
                    thickness=2, lineType=cv2.LINE_AA)
                cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                self.line.run()


# TEST CODE
id = 2 # Car ID changes its priority
decision = Decision(id)
if __name__ == '__main__':
    print('Decision algorithm is starting...')
    try:
        decision.run()
    except KeyboardInterrupt:  # Stop car when 'Ctrl+C'
        PWM.setMotorModel(0, 0, 0, 0)
