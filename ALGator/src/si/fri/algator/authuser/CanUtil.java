package si.fri.algator.authuser;

import java.util.List;

public class CanUtil {
    public static boolean can(final String uid, final String eid, final String codename) {
        if(uid.equals("u0")) {
            return true;
        }

        AuthuserDAO dao = new AuthuserDAO();
        EntitiesDTO e = dao.getEntity(eid);

        if(e.getOwner().equals(uid)){
            return true;
        }
        else if(e.isPrivate()){
            return false;
        }

        EntityPermissionUserDTO epu = dao.getEntityPermissionUser(uid, eid);
        PermissionTypeDTO p = dao.getPermissionType(codename);
        PermissionTypeDTO pfc = dao.getPermissionType("full_control");

        if (contains(epu.getValue(), p.getValue(), pfc.getValue())) {
            return true;
        }
        List<GroupDTO> groups = dao.getGroupsByUser(uid);

        for (int i = 0; i < groups.size(); i++) {
            String gid = groups.get(i).getId();
            EntityPermissionGroupDTO epg = dao.getEntityPermissionGroup(eid, gid);
            if(contains(epg.getValue(), p.getValue(), pfc.getValue())){
                return true;
            }
        }
        return false;
    }

    private static boolean contains(long id, long p, long pfc){
        return (id & p) == p || (id & pfc) == pfc;
    }

}
