// Name: Yoni Xiong
// Assignment: Final Project
// Date: 11/14/2020

import java.util.Map;
import java.util.HashMap;

public class MasterState {
    private Map<Integer, CarState> states; 

    public MasterState(){
        this.states = new HashMap<Integer, CarState>();
    }

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

    public CarState getCarState(int id){
        return this.states.get(id); 
    }

    public Map<Integer, CarState> getStates(){
        return states; 
    }
}
