// Name: Yoni Xiong
// Assignment: Final Project
// Date: 11/14/2020

import java.util.ArrayList;
import java.util.List;

public class CarState {
    private int CAR_ID; 
    private State carState; 

    public CarState(){
        this.CAR_ID = 0; 
        this.carState = new State(); 
    }
    public CarState(int id, State state){
        this.CAR_ID = id; 
        this.carState = state;
    }

    public CarState(int id, int direction, double speed, double ultra, int other, List<Double> locations){
        this.CAR_ID = id; 
        this.carState = new State(id, direction,speed,ultra,other,locations);
    }

    public CarState(int id, int direction, double speed, double ultra, int other, double x, double y, double r){
        this.CAR_ID = id; 
        this.carState = new State(id, direction,speed,ultra,other,null);
        setLocation(x, y, r);
    }

    public void updateState(String serialString){
        this.carState.updateState(serialString);
    }

    public void setCARID(int id){
        this.CAR_ID = id; 
        this.carState.setCAR_ID(id);
    }

    public void setDirection(int dir){
        this.carState.setDirection(dir);
    }

    public void setSpeed(double speed){
        this.carState.setSpeed(speed);
    }

    public void setUltrasonic(double ultra){
        this.carState.setUltrasonic(ultra);
    }

    public void setOtherCarsCount(int cnt){
        this.carState.setOtherCarsCount(cnt);
    }

    public void setLocation(double x, double y, double r){
        List<Double> list = new ArrayList<Double>(); 
        list.add(x); 
        list.add(y); 
        list.add(r); 
        this.carState.setLocations(list);
    }

    public int getCar_ID(){
        return CAR_ID;
    }

    public String toString(){
        return this.carState.toString();
    }
}
