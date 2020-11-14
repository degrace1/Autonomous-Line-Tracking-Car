# Network Protocol for Autonomous Car

## Goals: 
- Communicate status of cars
- Maintain collection of states for updates for each car 
- Have no sync issues
----
## Operation Specs:
### Main Function:
A carStruct var will be created and initialized in the main function for the car. All the functions we write will have that carState obj passed to it by reference.
The main function will also have to call a "**connectToServer**(IP, PORT)" function to establish the network connection for subsequent calls to server send/request functions.
### Updating:
The moving, ultrasound, and object detection functions will write and modify parameters in the carState. After all writes, these functions should call another function to update the state in the server: **sendStateToServer**(carState). The **sendStateToServer**(carState) function will not return anything.
### Reading:
The decision algorithm will read parameters of carState to make a decision. The decision algorithm should call a function to poll the server for the most updated state of the car before starting the decision making process. The states for other cars can be requested by using the appropriate CAR_ID or location by calling: **requestStateFromServer**(int CAR_ID) or **requestStateFromServer**(List location).
### carState member variables:
- **int** CAR_ID //integer that represents the ID of a car, we will have to initialize it to a fixed number in the main program.
- **int** direction //between 0-3, where 0 = forward, 1 = background, 2 = left, 3 = right
- **int** speed //value for speed of the car
- **int** ultrasonic //distance of object sensed by ultrasonic sensor
- **int** otherCarsCount  //number of other cars detected nearby using CV
- **List** carsNearbyLocation //list with location detected by the CV alg of a car nearby [x,y,r]
### carState functions
- init(self) // sets all member elements to 0 or null
- init(self, int direction, int speed, int ultrasonic, int otherCarCount, List carsNearby Location) //sets all var to passed in values 
- setDirection(int direction)
- setSpeed(int speed)
- setUltrasonic(int distance)
- setOtherCarsCount(int count)
- setCarsNearbyLocation(List [x1,y1,r1,x2,y2,r2,..])
- int getDirection()
- int getSpeed()
- int getUltrasonic()
- int getOtherCarsCount()
- List getCarsNearbyLocation()
- String serializeState() //generate serial string of all state params (comma seperated)
- updateState(String serialState) // update member var using serial response string from server
### Server Functionality for FYI: 
- Hashmap to map location to car_id -> (x,y,z) -> CAR_ID = 1
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
request_state_by_ID|car_id:String
request_state_by_location|location:String
*Login Example| type=log_in&car_id=1
*Send State Example  | type=send_state&state=1,0,5,4,1,2,2,2

---
### Contact Info: 
- Yoni Xiong : yoni.xiong@vanderbilt.edu

