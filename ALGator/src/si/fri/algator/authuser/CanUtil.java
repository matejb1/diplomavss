package si.fri.algator.authuser;

import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.UrlEncodedFormEntity;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ClassicHttpResponse;
import org.apache.hc.core5.http.NameValuePair;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.message.BasicNameValuePair;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

public class CanUtil {
    private HttpClient client = null;
    private String ACCESS_TOKEN = null;
    private String REFRESH_TOKEN = null;

    private final String BASE_URL = System.getenv("ALGATORWEB_BASE_URL");
    private final String DATABASE_USER = System.getenv("DATABASE_USER");
    private final String DATABASE_PASSWORD = System.getenv("DATABASE_PASSWORD");
    private long expirationTime = 0L;

    public CanUtil(){
        client = HttpClients.createDefault();
        this.init();
    }

    private void init()  {
        try {
            HttpPost request = new HttpPost(BASE_URL+"/api/token/");
            request.addHeader("Accept", "application/json");
            List<NameValuePair> params = new ArrayList<NameValuePair>(2);
            params.add(new BasicNameValuePair("username", this.DATABASE_USER));
            params.add(new BasicNameValuePair("password", this.DATABASE_PASSWORD));
            request.setEntity(new UrlEncodedFormEntity(params, StandardCharsets.UTF_8));
            ClassicHttpResponse response = (ClassicHttpResponse)client.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());

            JSONObject json = new JSONObject(responseBody);
            this.REFRESH_TOKEN = json.get("refresh").toString();
            this.ACCESS_TOKEN = json.get("access").toString();

            Base64.Decoder decoder = Base64.getUrlDecoder();
            String header = new String(decoder.decode(ACCESS_TOKEN.split("\\.")[1]));
            json = new JSONObject(header);
            this.expirationTime = Long.parseLong(json.get("exp").toString());
        } catch(Exception e){
            System.err.println(e.getMessage());
        }
    }

    private void obtainAccessToken(){
        try{
            HttpPost request = new HttpPost(BASE_URL+"/api/token/refresh/");
            request.addHeader("Accept", "application/json");
            List<NameValuePair> params = new ArrayList<NameValuePair>(1);
            params.add(new BasicNameValuePair("refresh", this.REFRESH_TOKEN));
            request.setEntity(new UrlEncodedFormEntity(params, StandardCharsets.UTF_8));
            ClassicHttpResponse response = (ClassicHttpResponse)client.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());

            JSONObject json = new JSONObject(responseBody);
            this.ACCESS_TOKEN = json.get("access").toString();

            Base64.Decoder decoder = Base64.getUrlDecoder();
            String header = new String(decoder.decode(this.ACCESS_TOKEN.split("\\.")[1]));
            json = new JSONObject(header);
            this.expirationTime = Long.parseLong(json.get("exp").toString());
        } catch(Exception e){
            System.err.println(e.getMessage());
        }


    }

    public boolean can(String uid, String eid, String pid) {
        long unixCurrentTime = System.currentTimeMillis() / 1000L;

        if(unixCurrentTime >= this.expirationTime)
            this.obtainAccessToken();

        boolean result = false;
        try {
            HttpPost request = new HttpPost(BASE_URL+"/permissions/can");
            request.addHeader("Accept", "application/json");
            request.addHeader("Authorization", String.format("Bearer %s", this.ACCESS_TOKEN));
            List<NameValuePair> params = new ArrayList<NameValuePair>(3);

            params.add(new BasicNameValuePair("uid", uid));
            params.add(new BasicNameValuePair("eid", eid));
            params.add(new BasicNameValuePair("pid", pid));

            request.setEntity(new UrlEncodedFormEntity(params, StandardCharsets.UTF_8));
            ClassicHttpResponse response = (ClassicHttpResponse)client.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());

            return Boolean.parseBoolean(responseBody.toLowerCase().trim());
        } catch(Exception e){
            System.err.println(e.getMessage());
        }
        return result;
    }

}
