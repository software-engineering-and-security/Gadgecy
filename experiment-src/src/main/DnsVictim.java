package main;

import org.burningwave.tools.net.DNSClientHostResolver;
import org.burningwave.tools.net.HostResolutionRequestInterceptor;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

public class DnsVictim {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        HostResolutionRequestInterceptor.INSTANCE.install(
          new DNSClientHostResolver("127.0.0.1", Integer.parseInt(args[1]))
        );
        FileInputStream fis = new FileInputStream(args[0]);
        ObjectInputStream ois = new ObjectInputStream(fis);
        ois.readObject();        
    }
}
