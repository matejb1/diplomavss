package si.fri.algator.authuser;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;
import spark.Request;

public class AuthuserHelper {

    static boolean isEmptyOrNull(String s) {
        return s == null || s.trim().isEmpty();
    }

    static boolean isStringValid(String prefix, String s) {
        return s.startsWith(prefix) && s.matches(String.format("^%s[0-9]+$", prefix));
    }

    public static String tryToGetToken(Request request){
        try{
            String token = null;
            if (request.headers().contains("Authorization")) {
                token = request.headers("Authorization").split(" ")[1];
            }
            return token;
        } catch (Exception e) {
            return null;
        }
    }

    static boolean verifyToken(final String token, String secret) {
        try {
            DecodedJWT jwt = JWT.decode(token);
            Algorithm algorithm = Algorithm.HMAC256(secret);
            JWTVerifier verifier = JWT.require(algorithm).build();
            DecodedJWT dd = verifier.verify(token);
            return true;
        } catch (JWTVerificationException jwte) {
            return false;
        }
    }

    static String getUserFromToken(String token) {
        try{
            DecodedJWT decodedToken = JWT.decode(token);
            return decodedToken.getClaims().get("uid").asString();
        }catch (Exception e) {
            return "u1";
        }
    }
}
