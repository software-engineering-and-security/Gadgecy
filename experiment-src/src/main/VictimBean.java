package main;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.Base64;

@ManagedBean(name = "victimBean")
@RequestScoped
public class VictimBean {

    public VictimBean() {this.text = "";}
    String text;
    String poc;
    public String getText() {
        return text;
    }
    public void setText(String text) {
        this.text = text;
    }

    public String deserialize() throws IOException, ClassNotFoundException {
        byte[] data = Base64.getUrlDecoder().decode(text);
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        this.text = ois.readObject().toString() + "_more";
        return "";
    }
    public String getPoc() throws IOException {
        Runtime.getRuntime().exec("touch /tmp/proof.txt");
        return "";
    }
}