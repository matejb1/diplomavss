package si.fri.algator.authuser;

import com.mysql.cj.exceptions.ConnectionIsClosedException;
import si.fri.algator.database.Database;
import si.fri.algator.global.ATLog;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import static si.fri.algator.authuser.AuthuserHelper.isEmptyOrNull;
import static si.fri.algator.authuser.AuthuserHelper.isStringValid;

class AuthuserDAO {

    private static final String QUERY_GET_ENTITY_BY_ID = " SELECT " + "   id, " + //
            "   name, " + //
            "   is_private, " +  //
            "   entity_type_id, " + //
            "   owner_id, " + //
            "   parent_id" + //
            " FROM " + //
            "   authuser_entities " + //
            " WHERE " + //
            "   id = ?";

    private static final String QUERY_GET_ENTITY_PERMISSION_GROUP_BY_UID_EID = " SELECT " + //
            "   id, " + //
            "   value, " + //
            "   entity_id, " + //
            "   user_id " + //
            " FROM " + //
            "   authuser_entitypermissionuser " + //
            " WHERE " + //
            "   user_id = ? " + //
            "   AND entity_id = ?";

    private static final String QUERY_GET_PERMISSION_TYPE_BY_EID = " SELECT " + //
            "   id, " + //
            "   name, " + //
            "   codename, " + //
            "   value " + //
            " FROM " + //
            "   authuser_permissiontype " + //
            " WHERE " + //
            "   codename = ?";

    private static final String QUERY_GET_GROUPS_BY_UID = "(" + //
            "   SELECT  " + //
            "     g.id,  " + //
            "     g.name,  " + //
            "     g.owner_id  " + //
            "   FROM  " + //
            "     authuser_group g  " + //
            "     JOIN authuser_group_user gu ON gu.group_id = g.id  " + //
            "   WHERE  " + //
            "     gu.user_id = ? " + //
            " )  " + //
            " UNION  " + //
            "   ( " + //
            "     SELECT  " + //
            "       g.id,  " + //
            "       g.name,  " + //
            "       g.owner_id  " + //
            "     FROM  " + //
            "       authuser_group g  " + //
            "     WHERE  " + //
            "       id = ? " + //
            "   ) ";


    private static final String QUERY_GET_ENTITY_PERMISSION_GROUP_BY_EID_GID = " SELECT " + //
            "   id, " + //
            "   value, " + //
            "   entity_id, " + //
            "   group_id " + //
            " FROM " + //
            "   authuser_entitypermissiongroup " + //
            " WHERE " + //
            "   entity_id = ? " + //
            "   AND group_id = ?";


    private static final String QUERY_GET_LATEST_EID = " SELECT " + //
            "   id " + //
            " FROM " + //
            "   authuser_entities " + //
            " ORDER BY " + //
            "   CAST( " + //
            "     SUBSTRING(id, 2) AS UNSIGNED " + //
            "   ) DESC " + //
            " LIMIT 1";


    private static final String INSERT_PROJECT = "INSERT INTO authuser_entities (id, name, entity_type_id, is_private, owner_id, parent_id) VALUES (?, ?, 'et1', ?, ?, ?)";

    /**
     * This function will get single entity from database.
     *
     * @param eid Entity ID
     * @return EntityDTO from table authuser_entities
     */
    protected EntitiesDTO getEntity(final String eid) {

        if (isEmptyOrNull(eid) || !isStringValid("e", eid)) {
            throw new IllegalArgumentException("eid is null or empty or isn't valid.");
        }

        Connection conn = Database.getConnectionToDatabase();

        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        EntitiesDTO entity = new EntitiesDTO();
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_ENTITY_BY_ID);
            stmt.setString(1, eid);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                entity.setId(rs.getString("id"));
                entity.setName(rs.getString("name"));
                entity.setPrivate(rs.getBoolean("is_private"));
                entity.setEntityType(rs.getString("entity_type_id"));
                entity.setOwner(rs.getString("owner_id"));
                entity.setParent(rs.getString("parent_id"));
            }
        } catch (Exception e) {
            ATLog.log("Problem at getting values from table 'authuser_entities'. Error: " + e.getMessage(), 0);
        }

        return entity;
    }

    /**
     * This method will return single entity permission user object from database.
     *
     * @param uid user id
     * @param eid entity id
     * @return single entity permission user object from database.
     */
    protected EntityPermissionUserDTO getEntityPermissionUser(final String uid, final String eid) {
        if (isEmptyOrNull(uid) || !isStringValid("u", uid) || isEmptyOrNull(eid) || !isStringValid("e", eid)) {
            throw new IllegalArgumentException("uid or eid is null or empty or isn't valid.");
        }

        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        EntityPermissionUserDTO epu = new EntityPermissionUserDTO();
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_ENTITY_PERMISSION_GROUP_BY_UID_EID);
            stmt.setString(1, uid);
            stmt.setString(2, eid);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                epu.setId(rs.getString("id"));
                epu.setValue(rs.getLong("value"));
                epu.setEntity(rs.getString("entity_id"));
                epu.setUser(rs.getString("user_id"));
            }
        } catch (Exception e) {
            ATLog.log("Problem at getting values from table 'authuser_entitypermissionuser'. Error: " + e.getMessage(), 0);
        }
        return epu;
    }

    /**
     * This method will return single instance of permision type object from database.
     *
     * @param codename Permission name --> codename
     * @return permission type from database
     */
    protected PermissionTypeDTO getPermissionType(final String codename) {

        if (isEmptyOrNull(codename)) {
            throw new IllegalArgumentException("uid or eid is null or empty or isn't valid.");
        }
        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        PermissionTypeDTO p = new PermissionTypeDTO();
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_PERMISSION_TYPE_BY_EID);
            stmt.setString(1, codename);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                p.setId(rs.getString("id"));
                p.setValue(rs.getLong("value"));
                p.setCodename(rs.getString("codename"));
                p.setName(rs.getString("name"));
            }
        } catch (Exception e) {
            ATLog.log("Problem at getting values from table 'authuser_permissiontype'. Error: " + e.getMessage(), 0);
        }
        return p;
    }

    /**
     * This method will get all groups where user belongs.
     *
     * @param uid User id
     * @return list of groups
     */
    protected List<GroupDTO> getGroupsByUser(final String uid) {

        if (isEmptyOrNull(uid) || !isStringValid("u", uid)) {
            throw new IllegalArgumentException("uid is null or empty or isn't valid.");
        }
        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        List<GroupDTO> groups = new ArrayList<>();
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_GROUPS_BY_UID);

            String everyoneOrAnonymous = "g0";
            if (uid.equals("u1")) {
                everyoneOrAnonymous = "g1";
            }

            stmt.setString(1, uid);
            stmt.setString(2, everyoneOrAnonymous);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                GroupDTO g = new GroupDTO();
                g.setId(rs.getString("id"));
                g.setName(rs.getString("name"));
                g.setOwner(rs.getString("owner_id"));
                groups.add(g);
            }
        } catch (Exception e) {
            ATLog.log("Problem at getting values from tables 'auhuser_group' AND 'authuser_group_user'. Error: " + e.getMessage(), 0);
        }
        return groups;
    }

    protected EntityPermissionGroupDTO getEntityPermissionGroup(final String eid, final String gid) {

        if (isEmptyOrNull(gid) || !isStringValid("g", gid) || isEmptyOrNull(eid) || !isStringValid("e", eid)) {
            throw new IllegalArgumentException("gid or eid is null or empty or isn't valid.");
        }
        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        EntityPermissionGroupDTO epg = new EntityPermissionGroupDTO();
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_ENTITY_PERMISSION_GROUP_BY_EID_GID);
            stmt.setString(1, eid);
            stmt.setString(2, gid);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                epg.setId(rs.getString("id"));
                epg.setGroup(rs.getString("group_id"));
                epg.setValue(rs.getLong("value"));
                epg.setEntity(rs.getString("entity_id"));
            }
        } catch (Exception e) {
            ATLog.log("Problem at getting values from tables 'authuser_entitypermissiongroup'. Error: " + e.getMessage(), 0);
        }
        return epg;
    }

    private String getNewLatestEid() {
        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }
        try {
            PreparedStatement stmt = conn.prepareStatement(QUERY_GET_LATEST_EID);
            ResultSet rs = stmt.executeQuery();
            String id = null;
            if (rs.next()) {
                id = rs.getString("id");
            }

            id = "u" + (Integer.parseInt(id.substring(1)) + 1);

            return id;
        } catch (Exception e) {
            return "e0";
        }
    }

    protected void addProject(final String owner, final String name, final boolean isPrivate, final String parent) {
        if (isEmptyOrNull(owner) || isEmptyOrNull(name) || !isStringValid("u", owner)) {
            throw new IllegalArgumentException("Owner or name is null, empty or isn't valid.");
        }

        Connection conn = Database.getConnectionToDatabase();
        if (conn == null) {
            throw new ConnectionIsClosedException("Connection is null.");
        }

        String parentEid = null;
        if (!isEmptyOrNull(parent) && isStringValid("e", parent)) {
            parentEid = parent;
        }

        String eid = getNewLatestEid();
        try {
            PreparedStatement stmt = conn.prepareStatement(INSERT_PROJECT);
            stmt.setString(1, eid);
            stmt.setString(2, name);
            stmt.setBoolean(3, isPrivate);
            stmt.setString(4, owner);
            stmt.setString(5, parentEid);
            stmt.execute();
        } catch (Exception e) {
            ATLog.log("Problem at inserting values into table 'authuser_entities'. Error: " + e.getMessage(), 0);
        }
    }

}
