import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class Message {
    // parameter formatting
    private static final String PARAM_DELIMITER = "&"; 
    private static final String PARAM_ASSIGNMENT = "="; 

    // types
    public static final String LOGIN_COMMAND = "log_in"; 
    public static final String LOGOUT_COMMAND = "log_out"; 
    public static final String REQ_STATE_COMMAND = "request_state"; 
    public static final String SEND_STATE_COMMAND = "send_state"; 
    public static final String SEND_ACK = "send_ack"; 

    // parameters 
    public static final String TYPE_KEY = "type";
    public static final String STATE_KEY = "state"; 
    public static final String ID_KEY = "car_id"; 
        
    // map to hold parameters 
    private Map<String, String> myParams; 

    // default ctor 
    // init empty map for email message
    public Message(){
        myParams = new HashMap<String, String>(); 
    }

    // alt ctor 
    // create email message using serialized string 
    public Message(String serialMessage){
        // extract params from message 
        myParams = extractParams(serialMessage);
    }

    // add param to map 
    public String putParam(String key, String value){
        return myParams.put(key,value); 
    }

    // get param value using key 
    public String getParam(String key){
        return myParams.get(key); 
    }

    // serialize all params into string 
    public String toString(){
        StringBuilder stringTemp = new StringBuilder(); 
        Set<String> keys = myParams.keySet(); 

        // init string and deliminter value 
        String delim = ""; 

        // build serial string of all keys and params in hashmap
        for (String key: keys){
            // separate key,value pairs with delim
            stringTemp.append(delim);

            // separate key and value with param assignment
            stringTemp.append(key + PARAM_ASSIGNMENT + myParams.get(key)); 
            delim = PARAM_DELIMITER;  
        }

        // return encoded message
        return stringTemp.toString(); 
    }

    private HashMap<String, String> extractParams (String serialMessage){

        // make empty hashmap to hold param key, value pairs in serial message
        HashMap<String, String> paramMap = new HashMap<String, String>(); 

        // extract pairs into array using delim 
        String[] pairs = serialMessage.split(PARAM_DELIMITER); 

        for (String pairKeyValue: pairs){
            // split pairs into key and value 
            String[] keyAndValue = pairKeyValue.split(PARAM_ASSIGNMENT, 2);
            
            // print error serial message formatted incorrectly 
            if (keyAndValue.length != 2){
                System.out.println("Formatting error in serial message"); 
            } 
            
            // put params into map 
            else {
                paramMap.put(keyAndValue[0], keyAndValue[1]); 
            }
        }

        // return filled map
        return paramMap; 
    }
}
