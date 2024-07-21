package si.fri.algator.authuser;

import si.fri.algator.global.ATLog;

import java.util.List;

import static si.fri.algator.authuser.AuthuserHelper.isEmptyOrNull;
import static si.fri.algator.authuser.AuthuserHelper.isStringValid;

public class CanUtil {

    /**
     * This function will return if some user has permission of doing something with certain entity.
     * @param uid user id
     * @param eid entity id
     * @param codename permission name
     * @return It returns true if user has that permission on this entity.
     */
    public static boolean can(final String uid, final String eid, final String codename) {

        if(isEmptyOrNull(uid) || isEmptyOrNull(eid) || isEmptyOrNull(codename) || !isStringValid("u", uid) || !isStringValid("e", eid)) {
            throw new IllegalArgumentException("can: At least one of argument is null or isn't valid.");
        }

        if(uid.equals("u0")) {
            return true;
        }

        AuthuserDAO dao = new AuthuserDAO();

        try {
            EntitiesDTO e = dao.getEntity(eid);

            if (e.getOwner().equals(uid)) {
                return true;
            } else if (e.isPrivate()) {
                return false;
            }

            EntityPermissionUserDTO epu = dao.getEntityPermissionUser(uid, eid);
            PermissionTypeDTO p = dao.getPermissionType(codename);
            if (contains(epu.getValue(), p.getValue())) {
                return true;
            }
            List<GroupDTO> groups = dao.getGroupsByUser(uid);

            for (int i = 0; i < groups.size(); i++) {
                String gid = groups.get(i).getId();
                EntityPermissionGroupDTO epg = dao.getEntityPermissionGroup(eid, gid);
                if (contains(epg.getValue(), p.getValue())) {
                    return true;
                }
            }
        } catch (Exception err) {
            ATLog.log("Exception occurred in can. Error: " + err.getMessage(), 0);
        }
        return false;
    }

    private static boolean contains(long id, long p){
        return (id & p) == p;
    }

}
