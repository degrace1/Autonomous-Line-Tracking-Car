import socket 
import time
ERRORVAL = 1
SUCCESS = 0
FAILED = 'failed'
class CarState: 
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
    def log(self):
        print("car id: " + str(self.id))
        print("direction: " + str(self.direction))
        print("speed: " + str(self.speed))
        print("other cars around: " + str(self.other))
        print("x: " + str(self.location[0]))
        print("y: " + str(self.location[1]))
        print("z: " + str(self.location[2]))
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
    def send(self, address, port):
        message = self.toString()
        Message.sendMessage(address, port, self.id, message)
    def recv_h(self, address, port):
        return (Message.recvMessage(address, port, self.id).decode('UTF-8').rstrip())
    def recvByID(address, port, int):
        return (Message.recvMessage(address, port, int).decode('UTF-8').rstrip())
    # returns string 'failed' if full message is not received from server.. retry until you dont get the failed msg
    def update_h(self, address, port, id):
        state = CarState.recvByID(address,port,id)
        stateString = Message.decodeMessage(state)
        if (stateString == FAILED):
            return ERRORVAL
        self.updateState(stateString)
        return 0
    def update(self, address, port, id):
        val = self.update_h(address, port, id)
        while (val == 10):
            val = self.update_h(address, port, id)
    def recv(self, address, port):
        val = self.recv_h(address, port)
        while (val == FAILED):
            val = self.recv_h(address, port)
                
class Message:
    def sendMessage(address, port, car_id, serialMessage):
        s = socket.socket()
        s.connect((address,port))
        # type=log_in&car_id=[car_id]\n
        login = 'type=log_in&car_id='
        login += str(car_id) + '\n'
        #type=send_state&state=[serialMessage]\n
        send = 'type=send_state&state='
        send += serialMessage +'\n'
        logout = 'type=logout\n'
        # login and send message
        s.sendall(login.encode('UTF-8'))
        s.sendall(send.encode('UTF-8'))
        s.sendall(logout.encode('UTF-8'))
        s.close()
    def recvMessage(address, port, car_id):
        s = socket.socket()
        s.connect((address,port))
        # type=log_in&car_id=[car_id]\n
        login = 'type=log_in&car_id='
        login += str(car_id) + '\n'
        recv = 'type=request_state\n'
        logout = 'type=logout\n'
        # login and recv message
        s.sendall(login.encode('UTF-8'))
        s.sendall(recv.encode('UTF-8'))
        time.sleep(0.15)
        serverMessage = s.recv(134217728)
        s.sendall(logout.encode('UTF-8'))
        s.close()
        if (len(serverMessage)<19): return FAILED.encode('utf-8')
        return serverMessage
    def decodeMessage(serialMessage):
        s = serialMessage.split('&')
        for i in s:
            pair = i.split('=')
            if (len(pair) != 2): return "failed"
            if (pair[0] == 'state'):
                return pair[1]
        


