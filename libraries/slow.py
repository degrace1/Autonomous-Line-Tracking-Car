import time
from Motor import *
import RPi.GPIO as GPIO
class Slow_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)

    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                PWM.setMotorModel(400, 400, 400, 400)
                self.direction = 1 # Forward
            elif self.LMR==4:
                PWM.setMotorModel(-750, -750, 1250, 1250)
                self.direction = 4 # Right
            elif self.LMR==6:
                PWM.setMotorModel(-1000, -1000, 2000, 2000)
                self.direction = 4 # Faster Right
            elif self.LMR==1:
                PWM.setMotorModel(1250, 1250, -750, -750)
                self.direction = 3 # Left
            elif self.LMR==3:
                PWM.setMotorModel(2000, 2000, -1000, -1000)
                self.direction = 3 # Faster Left
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(0,0,0,0)
                self.direction = 0
          
        # Direction of car: 0 is stopped, 1 is forward, 2 is backward, 3 is left, 4 is right
        def get_direction():
            return self.direction
            
infrared = Slow_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
