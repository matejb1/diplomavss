package si.fri.algator.authuser;

import si.fri.algator.database.Database;
import si.fri.algator.global.ATLog;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

class AuthuserDAO {
    protected EntitiesDTO getEntity(final String eid) {
        final String sql = "SELECT id, name, is_private, entity_type_id, owner_id, parent_id FROM authuser_entities WHERE id = ?";
        EntitiesDTO entity = new EntitiesDTO();
        try {
            PreparedStatement stmt = Database.getConnectionToDatabase().prepareStatement(sql);
            stmt.setString(1, eid);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                entity.setId(rs.getString("id"));
                entity.setName(rs.getString("name"));
                entity.setPrivate(rs.getBoolean("is_private"));
                entity.setEntityType(rs.getString("entity_type_id"));
                entity.setOwner(rs.getString("owner_id"));
                entity.setParent(rs.getString("parent_id"));
            }
        } catch (SQLException e) {
            ATLog.log("Problem at getting values from table 'authuser_entities'. Error: " + e.getMessage(), 0);
        }
        return entity;
    }

    protected EntityPermissionUserDTO getEntityPermissionUser(final String uid, final String eid) {
        final String sql = "SELECT id, value, entity_id, user_id FROM authuser_entitypermissionuser WHERE user_id = ? AND entity_id = ?";
        EntityPermissionUserDTO epu = new EntityPermissionUserDTO();
        try {
            PreparedStatement stmt = Database.getConnectionToDatabase().prepareStatement(sql);
            stmt.setString(1, uid);
            stmt.setString(2, eid);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                epu.setId(rs.getString("id"));
                epu.setValue(rs.getLong("value"));
                epu.setEntity(rs.getString("entity_id"));
                epu.setUser(rs.getString("user_id"));
            }
        } catch (SQLException e) {
            ATLog.log("Problem at getting values from table 'authuser_entitypermissionuser'. Error: " + e.getMessage(), 0);
        }
        return epu;
    }

    protected PermissionTypeDTO getPermissionType(final String codename) {
        final String sql = "SELECT id, name, codename, value FROM authuser_permissiontype WHERE codename = ?";
        PermissionTypeDTO p = new PermissionTypeDTO();
        try {
            PreparedStatement stmt = Database.getConnectionToDatabase().prepareStatement(sql);
            stmt.setString(1, codename);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                p.setId(rs.getString("id"));
                p.setValue(rs.getLong("value"));
                p.setCodename(rs.getString("codename"));
                p.setName(rs.getString("name"));
            }
        } catch (SQLException e) {
            ATLog.log("Problem at getting values from table 'authuser_permissiontype'. Error: " + e.getMessage(), 0);
        }
        return p;
    }

    protected List<GroupDTO> getGroupsByUser(final String uid) {
        final String sql = "(SELECT g.id, g.name, g.owner_id FROM authuser_group g JOIN authuser_group_user gu ON gu.group_id = g.id WHERE gu.user_id = ?) UNION (SELECT g.id, g.name, g.owner_id FROM authuser_group g WHERE id = ?)";
        List<GroupDTO> groups = new ArrayList<>();
        try {
            PreparedStatement stmt = Database.getConnectionToDatabase().prepareStatement(sql);
            stmt.setString(1, uid);
            stmt.setString(2, uid.equals("u1") ? "g1" : "g0");
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                GroupDTO g = new GroupDTO();
                g.setId(rs.getString("id"));
                g.setName(rs.getString("name"));
                g.setOwner(rs.getString("owner_id"));
                groups.add(g);
            }
        } catch (SQLException e) {
            ATLog.log("Problem at getting values from tables 'auhuser_group' AND 'authuser_group_user'. Error: " + e.getMessage(), 0);
        }
        return groups;
    }

    protected EntityPermissionGroupDTO getEntityPermissionGroup(final String eid, final String gid) {
        final String sql = "SELECT id, value, entity_id, group_id FROM authuser_entitypermissiongroup WHERE entity_id = ? AND group_id = ?";
        EntityPermissionGroupDTO epg = new EntityPermissionGroupDTO();
        try {
            PreparedStatement stmt = Database.getConnectionToDatabase().prepareStatement(sql);
            stmt.setString(1, eid);
            stmt.setString(2, gid);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                epg.setId(rs.getString("id"));
                epg.setGroup(rs.getString("group_id"));
                epg.setValue(rs.getLong("value"));
                epg.setEntity(rs.getString("entity_id"));
            }
        } catch (SQLException e) {
            ATLog.log("Problem at getting values from tables 'authuser_entitypermissiongroup'. Error: " + e.getMessage(), 0);
        }
        return epg;
    }

}
