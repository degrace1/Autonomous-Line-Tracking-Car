// Name: Yoni Xiong
// Assignment: Final Project
// Date: 11/14/2020

import java.util.Map;
import java.util.HashMap;

public class MasterState {

    // maps car identifier to carstate object
    private Map<Integer, CarState> states; 

    // constructor
    public MasterState(){
        this.states = new HashMap<Integer, CarState>();
    }

    // add a CarState to the map
    public void add(int id, String serialState){
        // check if car has a state already
        CarState temp = states.get(id); 
        // if not, make a new state
        if(temp == null){
            temp = new CarState(); 
            states.put(id, temp); 
        }
        // otherwise, update exisiting states
        temp.updateState(serialState); 
    }

    // return the CarState for a given car identifier 
    public CarState getCarState(int id){
        return this.states.get(id); 
    }

    // return the entire map
    public Map<Integer, CarState> getStates(){
        return states; 
    }
}
