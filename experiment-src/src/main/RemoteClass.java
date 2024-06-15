package main;

public class RemoteClass {

    public RemoteClass() throws Exception{
        Runtime.getRuntime().exec(new String[] {
            "touch", "proof_rmi.txt"
        });
    }     
}
