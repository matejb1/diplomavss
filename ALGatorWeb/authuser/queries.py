# Katere pravice entitet ima določen uporabnik ?
PERMISSIONS_ENTTIES_BY_USER = ("SELECT epu.id as id, epu.entity_id as entity_id, epu.permission_id as permission_id, "
                               "e.entity_id as entity_id_id, e.is_private as is_private, pt.name as pt_name, pt.codename as pt_codename "
                               "FROM authuser_entitypermissionuser epu "
                               "JOIN authuser_entities e ON e.id = epu.entity_id "
                               "JOIN authuser_permissiontype pt ON pt.id = epu.permission_id "
                               "WHERE epu.user_id = %s "
                               "ORDER BY id")

# Katere pravice entitet ima določena skupina ?
PERMISSIONS_ENTTIES_BY_GROUP = ("SELECT epg.id as id, epg.entity_id as entity_id, epg.permission_id as permission_id, "
                                "e.entity_id as entity_id_id, e.is_private as is_private, pt.name as pt_name, pt.codename as pt_codename "
                                "FROM authuser_entitypermissiongroup epg "
                                "JOIN authuser_entities e ON e.id = epg.entity_id "
                                "JOIN authuser_permissiontype pt ON pt.id = epg.permission_id "
                                "WHERE epg.group_id = %s "
                                "ORDER BY id ")

# Ali je uporabnik že v neki skupini ?
IS_THIS_USER_ALREADY_IN_GROUP = ("SELECT EXISTS( "
                                 "SELECT 1 "
                                 "FROM authuser_group_user "
                                 "WHERE group_id = %s AND user_id = %s "
                                 ") as exists_in_group")

# Pridobi podatke o entiteti in lastniku
ENTTITES_AND_OWNER = ("SELECT e.id as eid, e.entity_id as entity_id, e.is_private as is_private, "
                      "et.id as etid, et.name as name, u.id as uid, u.username "
                      "FROM authuser_entities e "
                      "JOIN authuser_entitytype et ON e.entity_type_id = et.id "
                      "JOIN auth_user u ON e.owner_id = u.id")

# Katere entitete pripadajo uporabniku ?
ENTTITES_BY_USER = ("SELECT e.id as eid, e.entity_id as entity_id, e.is_private as is_private, "
                    "et.id as etid, et.name as name "
                    "FROM authuser_entities e "
                    "JOIN authuser_entitytype et ON e.entity_type_id = et.id "
                    "WHERE e.owner_id = %s")

# Katere entitete pripadajo skupini ?
ENTTITES_BY_GROUP = ("SELECT e.id as eid, e.entity_id as entity_id, e.is_private as is_private, "
                     "et.id as etid, et.name as name "
                     "FROM authuser_entities e "
                     "JOIN authuser_entitytype et ON e.entity_type_id = et.id "
                     "WHERE e.owner_id = %s")

USER_HAS_THAT_PERMISSION = ("SELECT EXISTS(SELECT 1 " 
                            "FROM authuser_entitypermissionuser "
                            "WHERE user_id = %s AND entity_id = %s AND permission_id = %s) "
                            "as user_has_permission")

GROUP_HAS_THAT_PERMISSION = ("SELECT EXISTS(SELECT 1 " 
                            "FROM authuser_entitypermissiongroup "
                            "WHERE group_id = %s AND entity_id = %s AND permission_id = %s) "
                            "as group_has_permission")

PERMISSIONS_ENTTIES_USER_GROUP = ("(SELECT e.id as eid, epu.value as value, e.is_private as is_private, CONCAT('u: ', u.username) as user_group, epu.user_id as id " 
                                  "FROM authuser_entitypermissionuser epu " 
                                  "LEFT JOIN authuser_entities e ON e.id = epu.entity_id " 
                                  "JOIN authuser_user uu ON uu.id = epu.user_id " 
                                  "JOIN auth_user u ON u.id = uu.user_id " 
                                  "WHERE epu.user_id = %s) UNION " 
                                  "( SELECT e.id as eid, epg.value as value, e.is_private as is_private, CONCAT('g: ', g.name) as user_group, epg.group_id as id " 
                                  "FROM authuser_entitypermissiongroup epg " 
                                  "LEFT JOIN authuser_entities e ON e.id = epg.entity_id " 
                                  "JOIN authuser_group g ON g.id = epg.group_id " 
                                  "WHERE epg.group_id IN(SELECT group_id FROM authuser_group_user WHERE user_id = %s) ) ")


PERMISSIONS_ENTTIES_USER_GROUP_ROOT = ("(SELECT e.id as eid, epu.value as value, e.is_private as is_private, CONCAT('u: ', u.username) as user_group, epu.user_id as id " 
                                       "FROM authuser_entitypermissionuser epu " 
                                       "LEFT JOIN authuser_entities e ON e.id = epu.entity_id " 
                                       "JOIN authuser_user uu ON uu.id = epu.user_id " 
                                       "JOIN auth_user u ON u.id = uu.user_id) UNION " 
                                       "( SELECT e.id as eid, epg.value as value, e.is_private as is_private, CONCAT('g: ', g.name) as user_group, epg.group_id as id " 
                                       "FROM authuser_entitypermissiongroup epg " 
                                       "LEFT JOIN authuser_entities e ON e.id = epg.entity_id " 
                                       "JOIN authuser_group g ON g.id = epg.group_id " 
                                       "WHERE epg.group_id IN(SELECT group_id FROM authuser_group_user) ) ")




""" old 
PERMISSIONS_ENTTIES_USER_GROUP = ("(SELECT e.id as eid, CONV('FFFF',16,10) AS value, e.is_private as is_private, CONCAT('u: ', u.username) as user_group, uu.id as id " 
                                  "FROM authuser_entities e " 
                                  "JOIN authuser_user uu ON uu.id = e.owner_id " 
                                  "JOIN auth_user u ON u.id = uu.user_id " 
                                  "WHERE e.owner_id = %s) UNION "
                                  "(SELECT e.id as eid, epu.value as value, e.is_private as is_private, CONCAT('u: ', u.username) as user_group, epu.user_id as id " 
                                  "FROM authuser_entitypermissionuser epu " 
                                  "LEFT JOIN authuser_entities e ON e.id = epu.entity_id " 
                                  "JOIN authuser_user uu ON uu.id = epu.user_id " 
                                  "JOIN auth_user u ON u.id = uu.user_id " 
                                  "WHERE epu.user_id = %s) UNION " 
                                  "( SELECT e.id as eid, epg.value as value, e.is_private as is_private, CONCAT('g: ', g.name) as user_group, epg.group_id as id " 
                                  "FROM authuser_entitypermissiongroup epg " 
                                  "LEFT JOIN authuser_entities e ON e.id = epg.entity_id " 
                                  "JOIN authuser_group g ON g.id = epg.group_id " 
                                  "WHERE epg.group_id IN(SELECT group_id FROM authuser_group_user WHERE user_id = %s) ) ")
"""