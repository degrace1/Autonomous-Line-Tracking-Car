# Network Protocol for Autonomous Car

## Goals: 
- Communicate status of cars
- Maintain collection of states for updates for each car 
- Have no sync issues
----
## Operation Specs:
### Main Function:
A carStruct var will be created and initialized in the main function for the car. All the functions we write will have that carState obj passed to it by reference.

### How to make a CarState Obj: 
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
carStateEx = CarState(CAR_ID, direction, speed, ultrasonic, othercars, x, y, r); //note: no default constructer since python is cant have overloaded functions :(
```
### Updating:
The moving, ultrasound, and object detection functions will write and modify parameters in the carState. After all writes, these functions should call the **send** function to update the state in the server
```
// server IP address and port will be global constants at top of main file
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
    # handle it somehow -> redo?
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
- The message communcation reliablity is a bit hit or miss if the message is super long. It works well with my test "long" values but I can make it better with a delay in the recv function if it is not working well in our system. 
- Dont set the "other cars"value to anything other than 0 or 1!!!
----
### carState member variables:
- **int** CAR_ID //integer that represents the ID of a car, we will have to initialize it to a fixed number in the main program.
- **int** direction //between 0-4, 0 = idle, 1 = forward, 2 = background, 3 = left, 4 = right
- **double** speed //value for speed of the car 0 = stop, 1 = slow, 2 = medium, 3 = fast
- **double** ultrasonic //distance of object sensed by ultrasonic sensor -> alsex picks threshold
- **int** otherCarsCount  //number of other cars detected nearby using CV
- **List \<double>** carsNearbyLocation //list with location detected by the CV alg of a car nearby [x,y,r]
### carState functions
- init(self, int direction, int speed, int ultrasonic, int otherCarCount, List carsNearby Location) //sets all var to passed in values 
- setDirection(int direction)
- setSpeed(int speed)
- setUltrasonic(int distance)
- setOtherCarsCount(int count)
- setCarsNearbyLocation(List [x1,y1,r1,x2,y2,r2,..])
- int getDirection()
- double getSpeed()
- double getUltrasonic()
- int getOtherCarsCount()
- List<double> getCarsNearbyLocation()
- String serializeState() //generate serial string of all state params (comma seperated)
- updateState(String serialState) // update member var using serial response string from server
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
request_state|car_id:String
*Login Example| type=log_in&car_id=1
*Send State Example  | type=send_state&state=1,0,5,4,1,2,2,2

---
### Contact Info: 
- Yoni Xiong : yoni.xiong@vanderbilt.edu

