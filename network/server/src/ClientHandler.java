import java.io.BufferedReader; 
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.IOException; 
import java.net.Socket;

class ClientHandler implements Runnable { 
    private Socket myClientSocket;              // client socket
    private MasterState myCars;                 // cars
    private boolean killThrd; 
	
	// constructor 
    public ClientHandler(Socket myClientSocket, MasterState myStates) {
        // connect references to class members 
        this.myClientSocket = myClientSocket; 
        this.myCars = myStates; 
        this.killThrd = false;
	} 

	@Override
	public void run() {
        // run until token is invalid 
		while (!killThrd) { 
			try { 
                // reader and writer for client
                BufferedReader fromClient = new BufferedReader(new InputStreamReader(myClientSocket.getInputStream())); 
                DataOutputStream toClient = new DataOutputStream(myClientSocket.getOutputStream()); 

                // process the request
                processClientRequest(fromClient, toClient);

                // close resources
                try { 
                    fromClient.close(); 
                    toClient.close(); 
                    
                } catch(IOException e){ 
                    e.printStackTrace(); 
                }

			} catch (IOException e) { 
				
				e.printStackTrace(); 
			} 
			
		}  
    }
    
    public void processClientRequest(BufferedReader fromClient, DataOutputStream toClient) throws IOException {
        // init car_id for session
        String id = ""; 
        // quit bool
        boolean quit = false; 

        // service client until quit
        while(!quit){
            // read message from client
            String message = fromClient.readLine(); 

            if(message == null){
                this.killThrd = true; 
                quit = true; 
                return; 
            }
            // create message obj
            Message clientMessage = new Message(message); 

            // log client message 
            System.out.println("Recieved message: " + clientMessage.toString());

            // get type_key value
            String value = clientMessage.getParam(Message.TYPE_KEY); 

            // handle client commands 
            switch (value){
                case (Message.LOGIN_COMMAND):
                    // get car_id
                    id = clientMessage.getParam(Message.ID_KEY); 
                    break; 
                case (Message.SEND_STATE_COMMAND):
                    String state = clientMessage.getParam(Message.STATE_KEY); 
                    // add state
                    synchronized(myCars){
                        this.myCars.add(Integer.parseInt(id), state);
                    }
                    System.out.println("Added state: " + myCars.getStates().toString());
                    break; 
                case (Message.REQ_STATE_COMMAND):
                    Message stateToSend = new Message(); 
                    stateToSend.putParam(Message.TYPE_KEY, Message.SEND_STATE_COMMAND); 

                    // find state for car id 
                    synchronized (myCars){
                        CarState currState = this.myCars.getCarState(Integer.parseInt(id)); 
                        if (currState == null){
                            stateToSend.putParam(Message.STATE_KEY, "none"); 
                        }
                        else{
                            // create serial string 
                            String serialState = currState.toString(); 
                            stateToSend.putParam(Message.STATE_KEY, serialState);
                        }
                    }
                    // send state to client
                    toClient.writeBytes(stateToSend.toString() +'\n');
                    System.out.println("Sent: " + stateToSend.toString());
                    break; 
                case (Message.LOGOUT_COMMAND):
                    //quit program
                    killThrd = true; 
                    quit = true; 
                    break; 
            }
        }
        return;
    }
} 