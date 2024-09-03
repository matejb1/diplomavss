package si.fri.algator.authuser;

import org.json.JSONObject;
import si.fri.algator.server.ASLog;
import spark.Request;
import spark.Response;

import javax.naming.AuthenticationException;
import javax.naming.NoPermissionException;
import java.util.Set;
import java.util.zip.DataFormatException;

import static si.fri.algator.authuser.AuthuserHelper.isEmptyOrNull;
import static si.fri.algator.authuser.AuthuserHelper.isStringValid;
import static si.fri.algator.authuser.CanUtil.can;

public class AuthuserService {
    private static AuthuserDAO authuserDAO = new AuthuserDAO();

    public String addProject(Request req, Response res, String uid) {
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
            EntitiesDTO project = new EntitiesDTO();
            project.setName(data.getString("name"));
            project.setOwner(data.getString("owner"));
            project.setPrivate(true);
            project.setParent(null);

            if(keys.contains("is_private")){
                project.setPrivate(data.getBoolean("is_private"));
            }

            if(keys.contains("parent")){
                project.setParent(data.getString("parent"));
            }

            boolean can1 = can(project.getOwner(), "e0", "can_edit_rights");
            if(! uid.equals(project.getOwner()) && can1 && can(uid, "e0", "can_edit_rights") || uid.equals(project.getOwner()) && can1) {
                authuserDAO.addProject(project);
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
