# Autonomous-Line-Tracking-Car
### Team: 
Alex Feeley, Grace DePietro, Yoni Xiong, Yubo Du
### Goals: 
[]
### Instructions: 
[]
### Operation Specs: 
[]
### Libraries: 
[]

----
# Network Protocol for Autonomous Car

## Goals: 
- Communicate status of cars
- Maintain collection of states for updates for each car 
- Have no sync issues
----
## Operation Specs:
### Main Function:
A carStruct var will be created and initialized in the main function for the car. All the functions we write will have that carState obj passed to it by reference.

### How to make a CarState Object in Python: 
```
// import our class
from NetworkPackage import CarState, Message

// some random test vars for car conditions
CAR_ID = 10; 
direction = 4; 
speed = 3.14; 
ultrasonic = 6.9; 
othercars = 1; 
x = 9.0; 
y = 10.0; 
r = 11.0; 

// make object using car conditions
//note: no default constructer since python is cant have overloaded functions :(
carStateEx = CarState(CAR_ID, direction, speed, ultrasonic, othercars, x, y, r); 
```
### Updating:
The moving, ultrasound, and object detection functions will write and modify parameters in the carState. After all writes, these functions should call the **send** function to update the state in the server
```
// server IP address and port will be global constants at top of main file
// use hosted aws server w/ public ip when running
address = '127.0.0.1'
port = 6789

// call send function
carStateEx.send(address,port)
```
### Reading:
The decision algorithm will read parameters of carState to make a decision. The decision algorithm should call a function to poll the server for the most updated state of the a car by ID before starting the decision making process (if async in a thread but not if linear in a function). 
```
// loads temp with the state of CAR_ID from the server
tempCarObj = CarState(0, 0, 0, 0, 0, 0, 0, 0) 
tempCarObj.update(address,port,CAR_ID) 

// or, we can just update the state of an exisiting obj
error = carStateEx.update(address,port,carStateEx.getID) 
if (error != 0): 
    # handle it somehow -> means car polled server for had no state recorded
```
### Debugging: 
Use these log statements to see if the state is correct with what you expect: 
```
carStateEx.log()
/*
Log you will see printed to system console........ 
car id: 10
direction: 4
speed: 3.14
other cars around: 1
x: 9.0
y: 10.0
z: 11.0
*/

carStateEx.logInLine()
/*
Log you will see printed to system console........ 
car id =10,direction=4,speed=3.14,other cars around=1,x=9.0,y=10.0,z=11.0
*/
```

### Warnings: 
- Error (1) returned if you request state from a server for unregistered car
- Dont set the "other cars"value to anything other than 0 or 1!!!
----
### carState member variables:
- **int** CAR_ID //integer that represents the ID of a car, we will have to initialize it to a fixed number in the main program.
- **int** direction //between 0-4, 0 = idle, 1 = forward, 2 = background, 3 = left, 4 = right
- **double** speed //value for speed of the car 0 = stop, 1 = slow, 2 = medium, 3 = fast
- **double** ultrasonic //distance of object sensed by ultrasonic sensor -> alsex picks threshold
- **int** otherCarsCount  //number of other cars detected nearby using CV
- **List \<double>** carsNearbyLocation //list with location detected by the CV alg of a car nearby [x,y,r]
### carState functions:
- **init**(self, int direction, int speed, int ultrasonic, int otherCarCount, List carsNearby Location) //sets all var to passed in values 
- **setDirection**(int direction)
- **setSpeed**(int speed)
- **setUltrasonic**(int distance)
- **setOtherCarsCount**(int count)
- **setCarsNearbyLocation**(List [x1,y1,r1,x2,y2,r2,..])
- int **getDirection**()
- double **getSpeed**()
- double **getUltrasonic**()
- int **getOtherCarsCount**()
- List<double> **getCarsNearby**Location()
- String **serializeState**() //generate serial string of all state params (comma seperated)
- **updateState**(self, String serialState) // update member var using serial response string from server
- **syntax varies depending on Python or Java
### Server Functionality for FYI: 
- carState objects are stored for each registered CAR_ID.
- When a update is sent to the server, the appropriate car's object is updated.
- When a request is sent to the server, the appropriate car's object parameters are serialized and sent to the client.

----
## Serialized Commands to Communicate with Server: 
Key | Params 
------- | ----
log_in | car_id:String 
log_out|
send_state|state:String
send_ack|
request_state|car_id:String
*Login Example| type=log_in&car_id=1
*Send State Example  | type=send_state&state=1,0,5,4,1,2,2,2

---
### Contact Info: 
- Yoni Xiong : yoni.xiong@vanderbilt.edu

----
# Object Detection and Tracking for Autonomous Car

## Implement:

Instead of detecting the car iteslf, we put a colored ball on the top of each car and let the other smarts to detect and track it.

## Goals: 
- Detect the other cars (colored balls) in real time and return its pixel location in the image
- Given the radius of the detected ball, predict the distance
- Keep track of the colored ball
----

## Functions in object detection & tracking module
In the folder of libraries: BallCapture.py DistanceCamera.py

- **coloredBallTracking** (vs, yellowLower , yellowUpper , minR , maxR) in BallCapture.py

Before calling this function, videostream handler should be created first.

-- Input: vs: videostream handler, yellowLower: HSV space lower threshold of yellow color, yellowUpper: HSV space upper threshold of yellow color , minR: minimun ball size , maxR:maximum ball size. 'yellowLower' , 'yellowUpper' , 'minR' , 'maxR' they all have default settings and we do not have to change them.

-- Output: this function will return a list including [x,y,r], where x is the x axis pixel location of the ball center, y is the y axis pixel location of the ball center, r is the radius of the ball. When there is no ball detected it will return [0,0,0]


- **dVision** (radius) in DistanceCamera.py

-- Input: radius: radius of the ball.

-- Output: predicted distance of the ball (cm).

## Example for using detection & tracking module

```
from BallCapture import *
from ExampleCamera import *
from DistanceCamera import *
from imutils.video import VideoStream
import cv2
import imutils


#start video stream
#notice: the video stream should be created out of the loop
vs = VideoStream(src=0).start()
#warm up
time.sleep(2.0)

for i in range(1000):
    #calling coloredBallTracking()
    result = coloredBallTracking(vs)
    print(result)
    # if it detects a ball and retrun a non sero radius
    if result[2] != 0:
        #compute distance of the ball
        print(dVision(result[2]))

#close the camera and all windows
vs.stop()
cv2.destroyAllWindows() 
```

## How to test the camera
```
python camera.py

```
It  will pop up a window shows the capture of the video. Put the mouse on this window, press button 'q' in the keyboard, then the camera will be closed. The output video will be saved in the file named 'output.avi' in current folder.

**note:** To make the test more efficient, please test it in the same background and brightness as the demo. And put the colored ball before the camera and move it slowly. 

## Some advice for using this module

- It performs well when the background is simple, without any yellow color components. A good brightness with neither too strong nor too weak lightness is also prefered. 
- It may fail to detect the ball in some frames.
- It is very sensitive to the light and background. After moving on to a new background, we should adjust the parameters. again

### Contact Info: 
- Yubo Du : yubo.du@vanderbilt.edu

