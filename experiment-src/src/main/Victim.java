package main;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;


public class Victim {
    public static void main(String[] args) throws IOException, ClassNotFoundException {

        FileInputStream fis = new FileInputStream(args[0]);
        ObjectInputStream ois = new ObjectInputStream(fis);
        Object o = ois.readObject();

        ois.close();

    }
}