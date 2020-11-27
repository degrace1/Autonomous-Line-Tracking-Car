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

Instead of detecting the car iteslf, we put a colored ball on the top of each car and let the other smart cars to detect and track it.

## Goals: 
- Detect the other cars (colored balls) in real time and return its pixel location in the image.
- Given the radius of the detected ball, predict the distance (cm).
- Keep tracking of the colored ball and label it in the video.
----

## Class BallCapture

### BallCapture (self, yellowLower , yellowUpper , minR , maxR)
during the initialization hte class will open a video stream and set up all parameters.

Params | description 
------- | ----
vs |  videostream handler
yellowLower| lower threshold of yellow color in HSV
yellowUpper| upper threshold of yellow color in HSV
minR| minimun ball size
maxR| maximum ball size

'yellowLower' , 'yellowUpper' , 'minR' , 'maxR' they all have default settings and we do not have to change them.

### BallCapture.coloredBallTracking(): Capture the ball and return the location and radius 

- #### Output
This function will return a list [x,y,r]

Params | description 
------- | ----
x |   x axis pixel location of the ball center
y| y axis pixel location of the ball center
r| radius of the ball

When there is no ball detected it will return [0,0,0]


### BallCapture.dVision(radius) 

- #### Input
radius of the ball.

- #### Output
predicted distance of the ball (cm).

### BallCapture.captureOne()
This function assembles the coloedballTracking() and dVision(radius)
- #### Output
This function will return a list [x,y,r,distance],. When therre is no ball detected, it will return [0,0,0,-1]. 


### BallCapture.endAll()
End the video stream and close all windows.


## Example for using detection & tracking module

```
from BallCapture import *
from ExampleCamera import *
from DistanceCamera import *
from imutils.video import VideoStream
import cv2
import imutils


#initilize a ball capture class
c = BallCapture()

time.sleep(2.0)
for i in range(1000):
    #get the information of each frame
    print(c.captureOne())
#end the program
c.endAll()
```

you can also get the location of the ball and the distance seperately                                                           :

```
from BallCapture import *
from ExampleCamera import *
from DistanceCamera import *
from imutils.video import VideoStream
import cv2
import imutils


c = BallCapture()

time.sleep(2.0)
for i in range(1000):
    #get the information of each frame
    x,y,radius = c.captureOne()
    distance = c.dVision(radius)
    print(x,y,radius,distance)
#end the program
c.endAll()
```


## How to test the camera
```
python camera.py

```
It will pop up a window showing the capture of the video. Put the mouse on this window, press button 'q' in the keyboard, then the video will be terminated. The output video will be saved in the file named 'output.avi' in current folder.

**note:** To make the test more efficient, please test it in the same background and brightness as the demo. And put the colored ball before the camera with moving it slowly. 

## Some advices for using this module

- It performs well when the background is simple, without any yellow color components. A good brightness with neither too strong nor too weak lightness is also prefered. 
- It may fail to detect the ball in some frames but will work in most cases.
- It is very sensitive to the light and background. After moving on to a new background, we should adjust the parameters again.

### Contact Info: 
- Yubo Du : yubo.du@vanderbilt.edu