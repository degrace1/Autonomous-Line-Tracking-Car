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
        if True:
            self.LMR=0x00
            if GPIO.input(self.IR01) == True:
                self.LMR = (self.LMR | 4)
            if GPIO.input(self.IR02) == True:
                self.LMR = (self.LMR | 2)
            if GPIO.input(self.IR03) == True:
                self.LMR = (self.LMR | 1)
            if self.LMR == 2: # Forward
                PWM.setMotorModel(400, 400, 400, 400)
                self.direction = 1
            elif self.LMR == 4 or self.LMR == 6: # Right
                PWM.setMotorModel(-1500, -1500, 2500, 2500)
                self.direction = 4
            elif self.LMR == 1 or self.LMR == 3: # Left
                PWM.setMotorModel(2500, 2500, -1500, -1500)
                self.direction = 3
            elif self.LMR == 7: # Stop
                PWM.setMotorModel(0,0,0,0)
                self.direction = 0
          
    # Direction of car: 0 is stopped, 1 is forward, 2 is backward, 3 is left, 4 is right
    def get_direction(self):
        return self.direction

infrared = Slow_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print('Slow line tracking is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # Stop car when 'Ctrl+C'
        PWM.setMotorModel(0, 0, 0, 0)
