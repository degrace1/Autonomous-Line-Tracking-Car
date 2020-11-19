import time
from Motor import *
from Line_Tracking import *
from ultrasonic_sensor import Ultrasonic
from slow import Slow_Tracking
import RPi.GPIO as GPIO

class Decision:
    def __init__(self, car):
        self.car = CarState(car) # Initialize car state object
        self.line = Line_Tracking() # Car line follower algorithm
        self.ultra = Ultrasonic() # Ultrasonic methods
        
    def run(self):
        try:
            if car.getID == 0: # Car only traces line
                highPriority()
            elif car.getID == 1: # Car stops for one car or 5s
                mediumPriority()
            else: # Car stops until no cars are in view
                lowPriority()
        except KeyboardInterrupt: 
            PWM.setMotorModel(0, 0, 0, 0) # Car stops once control C pressed
    
    # Car has ID 0 and has the highest priority to the track. This car will follow
    # the line with no interruptions. 
    def highPriority(self):
        self.line.run()
    
    # Car has ID 1 and has the second highest priority to the track. This car will
    # follow the line. If the ultrasonic sensor detects an object within 30 cm, the
    # car will slow down until the car is at least 50 cm away. If the camera detects
    # an object not at the center of the frame, the car will stop until the object
    # is out of view or until 5 s has elapsed. 
    def mediumPriority(self):
        slow = Slow_Tracking()
        while True:
            if self.ultra.get_distance() < 30:
                slow.run()
            elif True: # Camera sees something to the side
                start = time.clock()
                update = start # Check if 5s has elapsed
                while True and update < 5: # While camera sees something to the side or 5 s has not elapsed
                    update = time.clock()
            else: # Nothing in the way, run normally
                self.line.run()
        
        
    def lowPriority(self):
        while True:
            if self.ultra.get_distance() < 30: # Or camera sees ANYTHING
                PWM.setMotorModel(0, 0, 0, 0) # Stop
            else:
                self.line.run()
