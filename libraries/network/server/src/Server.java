// Multhreaded Server
// Author: Yoni Xiong
// Purpose: map location to car id, store states of different cars, handle
// handle client requests (send/recieve), sync data so no overwriting issues, 
// UDP style where acks are not used due to high frequency of server updates. 

import java.io.IOException; 
import java.net.ServerSocket; 
import java.net.Socket;
import java.net.InetAddress;

// Server class 
public class Server { 
    // server port
    public static final int SERVER_PORT = 6789; 
	public static void main(String[] args) throws IOException 
	{ 
		// server is listening on port 1234 
		ServerSocket myServerSocket = new ServerSocket(SERVER_PORT); 
        // client socket
        Socket myClientSocket; 
        // states
        MasterState myInboxes = new MasterState();

		// running infinite loop for getting client requests 
		while (true) 
		{ 
            System.out.println("waiting for connection"); 

			// Accept the incoming request 
            myClientSocket = myServerSocket.accept(); 

            System.out.println("Connected!"); 

            InetAddress clientAddress = myClientSocket.getInetAddress(); 
            System.out.println("Client at: " + clientAddress.toString() + ":" + myClientSocket.getPort()); 
					            
			// Create a new handler object for handling this request. 
			ClientHandler request = new ClientHandler(myClientSocket, myInboxes); 

			// Create a new Thread with this object. 
			Thread thrd = new Thread(request); 
			
			// start the thread. 
			thrd.start();
        }
    } 
} 