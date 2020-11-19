import java.util.ArrayList;

public class StateDriver {
    public static void main(String[] args){
        ArrayList<Double> list = new ArrayList<Double>(); 
        list.add(1.1); 
        list.add(1.2); 
        list.add(1.3); 
        State test = new State(1,1,9.9,2.2,1,list); 
        System.out.println("test:" + test.toString());
        State test1 = new State(); 
        String tester = "1,1,9.8,2.1,1,1,1,1";
        test1.updateState(tester);
        System.out.println("test1:" +test1.toString());

        ///
        CarState test2 = new CarState(test.getCAR_ID(), test);
        System.out.println(test2.toString()+ " : should be same as test"); 
        CarState test3 = new CarState(test1.getCAR_ID(),1,9.8,2.2,1,list);
        System.out.println(test3.toString()+ " : should be same as test1"); 
        CarState test4 = new CarState(test.getCAR_ID(), 1,9.8,2.2,1, 1, 1, 1);
        System.out.println(test4.toString()+ " : should be same as test1"); 

        // are they indpendte? 
        // change test and chekc test 2
        test.setCAR_ID(15);
        if (test2.getCar_ID()!= 15){
            System.out.print("good"); 
        }
    } 

}
