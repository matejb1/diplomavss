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

    private static AuthuserDAO authuserDAO = new AuthuserDAO();
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
                return addProjectEndpointHandler(req, res, uid);
            default:
                ASLog.log("This endpoint ('" + fullPath + "') doesn't exits.");
                res.status(500);
                return "{\"Error\": \"This endpoint ('" + fullPath + "') doesn't exits.\"}";
        }
    }

    private String addProjectEndpointHandler(Request req, Response res, String uid) {
        try {
            if(isEmptyOrNull(uid) || !isStringValid("u", uid)) {
                ASLog.log("User needs to be login, before continuing following action.");
                throw new AuthenticationException("User needs to be login, before continuing following action.");
            }

            if(!req.body().startsWith("{")){
                ASLog.log("Error: Data isn't in JSON format.");
                throw new DataFormatException("Error: Data isn't in JSON format.");
            }

            JSONObject data = new JSONObject(req.body());
            Set<String> keys = data.keySet();

            if(!keys.contains("name") || !keys.contains("owner")) {
                ASLog.log("Error: Data doesn't contains name and owner");
                throw new IllegalArgumentException("Error: Data doesn't contains name and owner");
            }
            String name = data.getString("name");
            String owner = data.getString("owner");
            boolean isPrivate = true;
            String parent = null;

            if(keys.contains("is_private")){
                isPrivate = data.getBoolean("is_private");
            }

            if(keys.contains("parent")){
                parent = data.getString("parent");
            }

            boolean can1 = can(owner, "e0", "can_edit_rights");
            if(! uid.equals(owner) && can1 && can(uid, "e0", "can_edit_rights") || uid.equals(owner) && can1) {
                authuserDAO.addProject(owner, name, isPrivate, parent);
                res.status(201);
                ASLog.log("Added project successfully.");
            }
            else {
                ASLog.log("Permission denied.");
                throw new NoPermissionException("Permission denied.");
            }
            return "{\"Info\": \"OK\"}";
        }catch (Exception e) {
            res.status(500);
        }
        return "{\"Error\": \"Error occurred.\"}";
    }
}
