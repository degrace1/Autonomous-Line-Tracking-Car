import socket 
import time
ERRORVAL = 1
SUCCESS = 0
FAILED = 'failed'
NO_STATE = 'none'
THRESH = 5
class CarState: 

    # Constructor
    def __init__(self, id, dir, speed, ultra, other, x, y, r):
        self.id = id
        self.direction = dir
        self.speed = speed
        self.ultrasonic = ultra
        self.other = other
        self.location = []
        self.location.append(x)
        self.location.append(y)
        self.location.append(r)

    # all set methods for member variables 
    def setID(self, id):
        self.id = id
    def setDirection(self, dir):
        self.direction = dir
    def setSpeed(self,speed):
        self.speed = speed
    def setUltrasonic(self,ultra):
        self.ultrasonic = ultra
    def setOther(self, other):
        self.other = other
    def addLocation(self,x,y,r):
        self.location.append(x)
        self.location.append(y)
        self.location.append(r)
    def setLocation(self,x,y,r):
        self.location.clear()
        self.addLocation(x,y,r)

    # all get methods for member variables 
    def getID(self):
        return self.id
    def setDirection(self):
        return self.direction
    def setSpeed(self):
        return self.speed
    def setUltrasonic(self):
        return self.ultrasonic
    def setOther(self):
        return self.other
    def getLocation(self):
        return self.location

    # serialize state to string
    def toString(self):
        temp = ""
        delim = ","
        temp += str(self.id) + delim
        temp += str(self.direction) + delim
        temp += str(self.speed) + delim
        temp += str(self.ultrasonic) + delim
        temp += str(self.other)
        for i in self.location:
            temp += delim + str(i)
        return temp

    # show obj params in paragraph form 
    def log(self):
        print("car id: " + str(self.id))
        print("direction: " + str(self.direction))
        print("speed: " + str(self.speed))
        print("other cars around: " + str(self.other))
        print("x: " + str(self.location[0]))
        print("y: " + str(self.location[1]))
        print("z: " + str(self.location[2]))

    # show obj params in linear form 
    def logInLine(self):
        temp = ""
        delim = ","
        temp += "car id =" + str(self.id) + delim
        temp += "direction=" + str(self.direction) + delim
        temp += "speed=" + str(self.speed) + delim
        temp += "other cars around=" + str(self.other) + delim
        temp += "x=" + str(self.location[0]) + delim
        temp += "y=" + str(self.location[1]) + delim
        temp += "z=" + str(self.location[2])
        print(temp)

    # update the state of obj using serial state string from server
    def updateState(self, serialString):
        s = serialString.split(",")
        if (len(s) < 8): return ERRORVAL
        self.id = int(s[0]); 
        self.direction = int(s[1]); 
        self.speed = float(s[2]); 
        self.ultrasonic = float(s[3]); 
        self.other = int(s[4]); 
        self.location.clear()
        for i in range(self.other * 3):
           self.location.append(float(s[5+i]))
        return SUCCESS
    
    # send state for this obj to server
    def send(self, address, port):
        message = self.toString()
        Message.sendMessage(address, port, self.id, message)
   
    # get state string from server for this obj
    def recv(self, address, port):
        return (Message.recvMessage(address, port, self.id).rstrip())
    
    # get state string from server using id
    def recvByID(address, port, int):
        return (Message.recvMessage(address, port, int).rstrip())

    # returns ERRORVAL if server had no state for the car requested or if state could not be updated correctly
    def update(self, address, port, id):
        state = CarState.recvByID(address,port,id)
        stateString = Message.decodeMessage(state)
        if (stateString == NO_STATE):
            return ERRORVAL
        error = self.updateState(stateString)
        if (error == ERRORVAL): return ERRORVAL
        return SUCCESS
    # def update(self, address, port, id):
    #     counter = 0
    #     val = self.update_h(address, port, id)
    #     while (val == FAILED and counter < THRESH):
    #         val = self.update_h(address, port, id)
    #         counter += 1
    #     if (counter == THRESH):
    #         return ERRORVAL
    #     return SUCCESS
    # def recv(self, address, port):
    #     counter = 0
    #     val = self.recv_h(address, port)
    #     while (val == FAILED and counter < THRESH):
    #         val = self.recv_h(address, port)
    #         counter += 1
    #     if (counter == THRESH):
    #         return ERRORVAL
    #     return SUCCESS
                
class Message:

    # send state to server using id
    def sendMessage(address, port, car_id, serialMessage):
        # connect to socket 
        s = socket.socket()
        s.connect((address,port))

        # login: type=log_in&car_id=[car_id]\n
        login = 'type=log_in&car_id='
        login += str(car_id) + '\n'

        #send message: type=send_state&state=[serialMessage]\n
        send = 'type=send_state&state='
        send += serialMessage +'\n'
        logout = 'type=logout\n'

         # login. send message
        s.sendall(login.encode('UTF-8'))
        s.sendall(send.encode('UTF-8'))

        # get ack from server send before proceeding
        end_marker = '\n'
        buffer = ''
        while (True):
            buffer += (s.recv(1024)).decode('utf-8')
            if (end_marker in buffer) and (buffer == 'type=send_ack\n'):
                break
        
        #logout, and then close socket 
        s.sendall(logout.encode('UTF-8'))
        s.close()

    # poll server for state of car by id 
    def recvMessage(address, port, car_id):
        # connect to socket 
        s = socket.socket()
        s.connect((address,port))

        # login: type=log_in&car_id=[car_id]\n
        login = 'type=log_in&car_id='
        login += str(car_id) + '\n'

        # recv: type=request_state\n
        recv = 'type=request_state\n'

        # logout: 'type=logout\n
        logout = 'type=logout\n'

        # send login and recv message
        s.sendall(login.encode('UTF-8'))
        s.sendall(recv.encode('UTF-8'))

        # use loop to make sure all bytes till \n are read from adaptor 
        # do a max of 5 times to prevent inf loop ?
        end_marker = '\n'
        buffer = ''
        while (True):
            buffer += (s.recv(1024)).decode('utf-8')
            if end_marker in buffer:
                break
        
        # log out of server and close socket
        s.sendall(logout.encode('UTF-8'))
        s.close()

        # return serial state from buffer if mesage got to \n
        return buffer

    # decode serial state encoded in message 
    def decodeMessage(serialMessage):
        s = serialMessage.split('&')
        for i in s:
            pair = i.split('=')
            if (len(pair) != 2): return "failed"
            if (pair[0] == 'state'):
                return pair[1]
        


