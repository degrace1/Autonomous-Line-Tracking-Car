// Name: Yoni Xiong
// Assignment: Final Project
// Date: 11/14/2020

import java.util.ArrayList;
import java.util.List;


public class State {
    private int CAR_ID; 
    private int direction; 
    private double speed; 
    private double ultrasonic;
    private int otherCarsCount; 
    private List<Double> locations;
    private static String DELIM = ","; 

    public State(){
        this.CAR_ID = 0;
        this.direction = 0;
        this.speed = 0.0; 
        this.ultrasonic = 0.0; 
        this.otherCarsCount = 0;
        this.locations = new ArrayList<Double>(); 
    }
    public State(int CAR_ID, int direction, double speed, double ultra, int other, List<Double> locations){
        setCAR_ID(CAR_ID);
        setDirection(direction);
        setSpeed(speed);
        setUltrasonic(ultra);
        setOtherCarsCount(other);
        setLocations(locations);
    }

    public String toString(){
        StringBuilder stringTemp = new StringBuilder(); 
        String delim = DELIM; 
        stringTemp.append(CAR_ID);
        stringTemp.append(delim);
        stringTemp.append(direction);
        stringTemp.append(delim);
        stringTemp.append(speed);
        stringTemp.append(delim);
        stringTemp.append(ultrasonic);
        stringTemp.append(delim);
        stringTemp.append(otherCarsCount);
        for(double num: locations){
            stringTemp.append(delim);
            stringTemp.append(num);
        }
        return stringTemp.toString(); 
    }

    public void updateState(String serialString){
        String[] params = serialString.split(","); 
        this.CAR_ID = Integer.parseInt(params[0]);
        this.direction = Integer.parseInt(params[1]);
        this.speed = Double.parseDouble(params[2]);
        this.ultrasonic = Double.parseDouble(params[3]);
        this.otherCarsCount = Integer.parseInt(params[4]);
        this.locations.clear();
        for (int i = 0; i < otherCarsCount * 3; i++){
            this.locations.add(Double.parseDouble(params[5 + i]));
        }
    }

    // get x,y,z form
    public String locationToString(){
        StringBuilder stringTemp = new StringBuilder(); 
        String delim = ""; 
        for(double num: locations){
            stringTemp.append(delim);
            stringTemp.append(num);
            delim = DELIM;
        }
        return stringTemp.toString(); 
    }

    public void setCAR_ID(int cAR_ID) {
        CAR_ID = cAR_ID;
    }
    public void setDirection(int direction) {
        this.direction = direction;
    }
    public void setSpeed(double speed) {
        this.speed = speed;
    }
    public void setUltrasonic(double ultrasonic) {
        this.ultrasonic = ultrasonic;
    }
    public void setOtherCarsCount(int otherCarsCount) {
        this.otherCarsCount = otherCarsCount;
    }
    public void setLocations(List<Double> locations) {
        this.locations = locations;
    }
    public int getCAR_ID() {
        return CAR_ID;
    }
    public int getDirection() {
        return direction;
    }
    public double getSpeed() {
        return speed;
    }
    public double getUltrasonic() {
        return ultrasonic;
    }
    public int getOtherCarsCount() {
        return otherCarsCount;
    }
    // (x,y,z)
    public List<Double> getLocations() {
        return locations;
    }
}
