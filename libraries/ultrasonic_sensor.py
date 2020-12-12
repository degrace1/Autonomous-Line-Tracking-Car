import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
class Ultrasonic:
    def __init__(self): #initiate and set upnpins for i/o
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    def send_trigger_pulse(self): #sends out an ultrasonic wave forwards
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout): #waits for wave to come bounce back
        count = timeout
        #change count to understand distance
        while GPIO.input(self.echo_pin) != value and count>0: 
            count = count-1
     
    def get_distance(self):        #calculate distance
        distance_cm=[0,0,0,0,0]    #initial distance 0
        for i in range(3):         #loop 3x
            self.send_trigger_pulse()       #send a trigger pulse to start wave
            self.wait_for_echo(True,10000)  #wait for echo to come back
            start = time.time()             #start timer
            self.wait_for_echo(False,10000) #wait for echo
            finish = time.time()            #finish timer
            pulse_len = finish-start        #calc total time from lengths
            # multiply by usonic speed and divide by two (for there and back
            distance_cm[i] = (pulse_len * 34300) / 2 
        distance_cm=sorted(distance_cm)     #sort
        return int(distance_cm[2])          #return distance
