import time
from Motor import *
from Line_Tracking import *
from slow import Slow_Tracking
from NetworkPackage import *

class Decision:
    def __init__(self, id):
        self.car = CarState(id) # Initialize car state object
        self.line = Line_Tracking() # Car line follower algorithm
        self.time = time.time()
    
    def run(self):
        try:
            if self.car.getID == 0: # Car only traces line
                self.highPriority()
            elif self.car.getID == 1: # Car stops for one car or 5s
                self.mediumPriority()
            else: # Car stops until no cars are in view
                self.lowPriority()
        except KeyboardInterrupt: 
            PWM.setMotorModel(0, 0, 0, 0) # Car stops once control C pressed
            
    # Car has ID 0 and has the highest priority to the track. This car will follow
    # the line with no interruptions. 
    def highPriority(self):
        self.line.run()
    
    # Car has ID 1 and has the second highest priority to the track. This car will
    # follow the line. If the ultrasonic sensor detects an object within 30 cm, the
    # car will slow down until the car is at least 50 cm away. If the camera detects
    # an object, the car will stop until the object is out of view or until 5 s has elapsed.
    def mediumPriority(self):
        slow = Slow_Tracking()
        while True:
            if self.car.getUltrasonic < 30: # Ultrasonic sensor detects an object that is close
                while self.car.getUltrasonic < 50:
                    slow.run()
            elif True: # Camera detects an object that is close
                start = time.time()
                update = time.time()
                while True or update - start < 5: # While camera sees something to the side or 5 s has not elapsed
                    PWM.setMotorModel(0, 0, 0, 0)
                    update = time.time()
                    # get distance from camera
            else: # Nothing in the way, run normally
                self.line.run()

    # Car has ID 2 and has the third highest priority to the track. This car will follow
    # the line. If the ultrasonic sensor detects an object within 30 cm, the car will stop
    # until it's at least 50 cm away. If the camera de
    def lowPriority(self):
        while True:
            if self.car.getUltrasonic() < 30: # Ultrasnoic sensor detects that an object is close
                while self.car.getUltrasonic < 50:
                    PWM.setMotorModel(0, 0, 0, 0) # Stop
            elif True: # Camera detects that an object is close
                while True: #FIXME - distance to car must be less than 50 cm-ish
            else: # Nothing in the way, run normally
                self.line.run()       


## TEST CODE
id = 0 # Car ID changes its priority
decision = Decision(id)
if __name__ == '__main__':
    print('Decision algorithm is starting...')
    try:
        decision.run()
    except KeyboardInterrupt:  # Stop car when 'Ctrl+C'
        PWM.setMotorModel(0, 0, 0, 0)