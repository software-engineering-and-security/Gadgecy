package main;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.Base64;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class VictimApi extends HttpServlet{

   @Override
   public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException{

        JsonObject json = new Gson().fromJson(request.getReader(), JsonObject.class);
        
        String text = json.get("text").getAsString();
        
        byte[] data = Base64.getUrlDecoder().decode(text);
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        
        try {
            response.getOutputStream().println(ois.readObject().toString());
        } catch (Exception e) {
         response.getOutputStream().println(e.toString());
        }
        
   }  


} 