package si.fri.algator.authuser;

import org.json.JSONObject;
import si.fri.algator.server.ASLog;
import spark.Request;
import spark.Response;

import javax.naming.AuthenticationException;
import javax.naming.NoPermissionException;
import java.util.Set;
import java.util.zip.DataFormatException;

import static si.fri.algator.authuser.AuthuserHelper.*;
import static si.fri.algator.authuser.CanUtil.can;

public class AuthuserController {
    private static AuthuserService authuserService = new AuthuserService();

    private static final String SECRET_KEY = "django-insecure-5_0$q%!57#_5%vep30rg-_%!k5z7c*q*4=z3h%k(b&@2g6q((7";
    public String post(Request req, Response res){
        String fullPath = req.pathInfo().toUpperCase();
        String endpoint = fullPath.substring(fullPath.indexOf("/", 1));

        res.header("Content-type", "application/json");
        res.type("application/json");

        String token = tryToGetToken(req);
        String uid = "u1";
        if(!isEmptyOrNull(token) && verifyToken(token, SECRET_KEY)){
            uid = getUserFromToken(token);
        }

        switch (endpoint) {
            case "/ADDPROJECT":
                return authuserService.addProject(req, res, uid);
            default:
                ASLog.log("This endpoint ('" + fullPath + "') doesn't exits.");
                res.status(500);
                return "{\"Error\": \"This endpoint ('" + fullPath + "') doesn't exits.\"}";
        }
    }

}
