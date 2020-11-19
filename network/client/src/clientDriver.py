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
CAR_ID = 10000000; 
direction = 4000000; 
speed = 5; 
ultrasonic = 10000000; 
othercars = 1; 
x = 1990099; 
y = 1009999; 
r = 1990099; 

# static values 
# address = '100.26.217.199'
address = '127.0.0.1'
port = 6789

# log test values 
print()
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
print()
error = carState1.update(address,port, CAR_ID)
if (error == 1):
    print("error - 1")
    error = carState1.update(address,port, CAR_ID)
else: 
    print("Server info on car 1")
    print(carState1.toString())

# edit location of state 2
carState2.setLocation(1,1,1)
carState2.send(address,port)
print()
print("Server info on car 2")
print(carState2.toString())

# request state of different car from user (by id)
print()
error = carState2.update(address,port,CAR_ID)
if (error == 1):
    print("error - 2")
else:
    print("Overwrite state of car 2 w/ car 1")
    print(carState2.toString())

# request state of !unknown! car from user (by id)
print()
error = carState2.update(address,port,100)
if (error == 1):
    print("error - 3 - expected so good")
else:
    print("Overwrite state of car 2 w/ car 10000")
    print(carState2.toString())

# request state of yourself
print()
error = carState2.recv(address,port)
if (error == 1):
    print("error - 4")
else: 
    print("Poll car 2 state (revc)")
    print(carState2.toString())

# request state of yourself
print()
error = carState2.update(address,port,carState2.getID())
if (error == 1):
    print("error - 5")
else: 
    print("Poll car 2 state (update)")
    print(carState2.toString())

# test log format
print()
carState1.log()
print()
carState1.logInLine()
print()

#TODO: test on pi w/ aws server and hotspot 
# if still failing then put the time.sleep back in the NetworkPackage file




