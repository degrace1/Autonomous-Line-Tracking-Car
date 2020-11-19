import java.io.BufferedReader; 
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.IOException; 
import java.net.Socket;

public class ClientTest {
    // host address
    private static final String HOST_ADDRESS = "127.0.0.1";  
    // port              
    private static final int PORT = 6789; 

    public static void main(String[] args) throws IOException{
        // create new socket obj
        Socket socket = new Socket(HOST_ADDRESS, PORT); 

        // create new data output and input stream for server 
        DataOutputStream toServer = new DataOutputStream(socket.getOutputStream()); 
        BufferedReader fromServer = new BufferedReader(new InputStreamReader(socket.getInputStream())); 

        // create test values 
        int CAR_ID = 10; 
        int direction = 4; 
        double speed = 3.14; 
        double ultrasonic = 6.9; 
        int othercars = 1; 
        double x = 9; 
        double y = 10; 
        double r = 11; 
        System.out.println("Test Values for State"); 
        System.out.println("CAR_ID = " + CAR_ID); 
        System.out.println("direction = " + direction); 
        System.out.println("speed = " + speed); 
        System.out.println("ultrasonic = " + ultrasonic); 
        System.out.println("othercars = " + othercars); 
        System.out.println("x = " + x); 
        System.out.println("y = " + y); 
        System.out.println("r = " + r); 
        CarState testCar = new CarState(CAR_ID, direction, speed, ultrasonic, othercars, x, y, r); 

        // login1 to server 
        Message login = new Message(); 
        login.putParam(Message.TYPE_KEY, Message.LOGIN_COMMAND); 
        login.putParam(Message.ID_KEY, Integer.toString(CAR_ID)); 
        toServer.writeBytes(login.toString()+ '\n'); 

        // send state to server
        Message send = new Message(); 
        send.putParam(Message.TYPE_KEY, Message.SEND_STATE_COMMAND); 
        send.putParam(Message.STATE_KEY, testCar.toString()); 
        toServer.writeBytes(send.toString()+ '\n'); 
        System.out.println("Sent to server: " + send.toString()); 

        // requesst state from server 
        Message req = new Message(); 
        req.putParam(Message.TYPE_KEY, Message.REQ_STATE_COMMAND);
        toServer.writeBytes(req.toString()+ '\n'); 
        String responseFromServer = fromServer.readLine();  
        Message recvState = new Message(responseFromServer);
        System.out.println("Recieved State from server: " + recvState.toString()); 

        // log out
        Message logout = new Message(); 
        logout.putParam(Message.TYPE_KEY, Message.LOGOUT_COMMAND); 
        toServer.writeBytes(logout.toString()+ '\n'); 
    }
}
