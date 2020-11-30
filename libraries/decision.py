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
    def __init__(self, id):
        self.car = CarState(id,0,0,0,0,0,0) # Initialize car state object
        self.line = Line_Tracking() # Car line follower algorithm
        self.time = time.time()
        self.vs =VideoStream(src=0).start()
        self.BallTrack = BallCapture(vs = self.vs) #init the object detection class
        dir = 'frame'
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        
    def run(self):
        try:
            if self.car.getID() == 0: # Car only traces line
                print('the car is high priority')
                self.highPriority()
                
            elif self.car.getID() == 1: # Car stops for one car or 5s
                print('the car is medium priority')
                self.mediumPriority()
                
            else: # Car stops until no cars are in view
                print('the car is low priority')
                self.lowPriority()
                
        except KeyboardInterrupt: 
            PWM.setMotorModel(0, 0, 0, 0) # Car stops once control C pressed
            
    # Car has ID 0 and has the highest priority to the track. This car will follow
    # the line with no interruptions. 
    def highPriority(self):
        print("Priority of the car is high, just keep running!")
        self.line.run()
    
    # Car has ID 1 and has the second highest priority to the track. This car will
    # follow the line. If the ultrasonic sensor detects an object within 30 cm, the
    # car will slow down until the car is at least 50 cm away. If the camera detects
    # an object, the car will stop until the object is out of view or until 5 s has elapsed.
    def mediumPriority(self):
        slow = Slow_Tracking()
        while True:
            if False:#self.car.getUltrasonic() < 30: # Ultrasonic sensor detects an object that is close
                print("ultrasonic finds an object near!","distance = ", self.car.getUltrasonic())
                while self.car.getUltrasonic() < 50:
                    print("the object is still close (from ultrasonic)!","distance = ", self.car.getUltrasonic())
                    frame = self.vs.read()
                    cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                    slow.run()
            elif self.BallTrack.captureOne()[3] < 30 : # Camera detects an object that is close
                print("camera finds an object near!")
                start = time.time()
                update = time.time()
                while (self.BallTrack.captureOne()[3] < 30 ) or update - start < 5: # While camera sees something to the side or 5 s has not elapsed
                    print("the object is still close!")
                    PWM.setMotorModel(0, 0, 0, 0)
                    update = time.time()
                    # get distance from camera
            else: # Nothing in the way, run normally
                frame = self.vs.read()
                cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                print("keep running!")
                self.line.run()
                
                
    # Car has ID 2 and has the third highest priority to the track. This car will follow
    # the line. If the ultrasonic sensor detects an object within 30 cm, the car will stop
    # until it's at least 50 cm away. If the camera de
    def lowPriority(self):
        while True:
            if self.car.getUltrasonic() < 30: # Ultrasnoic sensor detects that an object is close
                print("ultrasonic finds an object near!","distance = ", self.car.getUltrasonic())
                while self.car.getUltrasonic() < 50:
                    print("the object is still close (from ultrasonic)!","distance = ", self.car.getUltrasonic())
                    frame = self.vs.read()
                    cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                    PWM.setMotorModel(0, 0, 0, 0) # Stop
            elif self.BallTrack.captureOne()[3] < 30 : # Camera detects that an object is close
                print("camera finds an object near!")
                while self.BallTrack.captureOne()[3] < 50 : #FIXME - distance to car must be less than 50 cm-ish
                    print("the object is still close!")
                    PWM.setMotorModel(0, 0, 0, 0)
            else: # Nothing in the way, run normally
                print("nothing in the way, keep running!")
                frame = self.vs.read()
                cv2.imwrite("frame//"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg',frame)
                self.line.run()
                


## TEST CODE
id = 1 # Car ID changes its priority
decision = Decision(id)
if __name__ == '__main__':
    print('Decision algorithm is starting...')
    try:
        decision.run()
    except KeyboardInterrupt:  # Stop car when 'Ctrl+C'
        PWM.setMotorModel(0, 0, 0, 0)