PERMISSIONS_ENTTIES_USER_GROUP = ("(SELECT e.id as eid, epu.value as value, e.is_private as is_private, CONCAT('u: ', uu.username) as user_group, epu.user_id as id " 
                                  "FROM authuser_entitypermissionuser epu " 
                                  "LEFT JOIN authuser_entities e ON e.id = epu.entity_id " 
                                  "JOIN authuser_user uu ON uu.uid = epu.user_id " 
                                  "WHERE epu.user_id = %s) UNION " 
                                  "( SELECT e.id as eid, epg.value as value, e.is_private as is_private, CONCAT('g: ', g.name) as user_group, epg.group_id as id " 
                                  "FROM authuser_entitypermissiongroup epg " 
                                  "LEFT JOIN authuser_entities e ON e.id = epg.entity_id " 
                                  "JOIN authuser_group g ON g.id = epg.group_id " 
                                  "WHERE epg.group_id IN(SELECT group_id FROM authuser_group_user WHERE user_id = %s) ) ")


PERMISSIONS_ENTTIES_USER_GROUP_ROOT = ("(SELECT e.id as eid, epu.value as value, e.is_private as is_private, CONCAT('u: ', uu.username) as user_group, epu.user_id as id "
                                       "FROM authuser_entitypermissionuser epu " 
                                       "LEFT JOIN authuser_entities e ON e.id = epu.entity_id " 
                                       "JOIN authuser_user uu ON uu.uid = epu.user_id ) "
                                       "UNION " 
                                       "(SELECT e.id as eid, epg.value as value, e.is_private as is_private, CONCAT('g: ', g.name) as user_group, epg.group_id as id " 
                                       "FROM authuser_entitypermissiongroup epg " 
                                       "LEFT JOIN authuser_entities e ON e.id = epg.entity_id " 
                                       "JOIN authuser_group g ON g.id = epg.group_id ) ")



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