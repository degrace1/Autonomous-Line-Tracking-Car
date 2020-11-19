# Test Code for server/client functionality
from NetworkPackage import CarState, Message
import socket 

# add some test values 
CAR_ID = 10; 
direction = 4; 
speed = 3.14; 
ultrasonic = 6.9; 
othercars = 1; 
x = 9.0; 
y = 10.0; 
r = 11.0; 

# add some LONGER test values 
# CAR_ID = 100000; 
# direction = 40000; 
# speed = 5; 
# ultrasonic = 100000; 
# othercars = 1; 
# x = 19999; 
# y = 19999; 
# r = 19999; 

# static values 
# address = '100.26.217.199'
address = '127.0.0.1'
port = 6789

# log test values 
print("Test Values for State"); 
print("CAR_ID = " + str(CAR_ID)); 
print("direction = " + str(direction)); 
print("speed = " + str(speed)); 
print("ultrasonic = " + str(ultrasonic)); 
print("othercars = " + str(othercars)); 
print("x = " + str(x)); 
print("y = " + str(y)); 
print("r = " + str(r)); 
carState1 = CarState(CAR_ID, direction, speed, ultrasonic, othercars,x,y,r); 
carState2 = CarState(0, 0, 0, 0, 0, 0, 0, 0) 

# send state 1 to server 
carState1.send(address,port)
carState2.send(address,port)

# request state from server 
error = carState1.update(address,port, CAR_ID)
if (error == 1):
    print("error!")
else: 
    print("Server info on car 1")
    print(carState1.toString())

# edit location of state 2
# carState2.setLocation(1,1,1)
# carState2.send(address,port)
# print("Server info on car 2")
# print(carState2.toString())

# request state of different car from user (by id)
error = carState2.update(address,port,CAR_ID)
if (error == 1):
    print("error!")
else:
    print("Overwrite state of car 2 w/ car 1")
    print(carState2.toString())

# request state of yourself
error = carState2.recv(address,port)
if (error == 1):
    print("error!")
else: 
    print("Poll car 2 state (revc)")
    print(carState2.toString())

# request state of yourself
error = carState2.update(address,port,carState2.getID())
if (error == 1):
    print("error!")
else: 
    print("Poll car 2 state (update)")
    print(carState2.toString())

# test log format
# carState1.log()
# carState1.logInLine()

#TODO: test on pi w/ aws server and hotspot 
# if still failing then put the time.sleep back in the NetworkPackage file




