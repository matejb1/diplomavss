USE algator;

ALTER TABLE authuser_entities CHANGE COLUMN is_private is_private BOOL NOT NULL DEFAULT TRUE;
ALTER TABLE authuser_entities DROP CONSTRAINT authuser_entities_parent_id_f86a251d_fk_authuser_entities_id;
ALTER TABLE authuser_entities ADD CONSTRAINT entiteta_omejitev FOREIGN KEY(parent_id) REFERENCES authuser_entities(id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE authuser_entitypermissiongroup DROP CONSTRAINT authuser_entitypermi_entity_id_214eee19_fk_authuser_;
ALTER TABLE authuser_entitypermissiongroup ADD CONSTRAINT entiteta_omejitev_epg FOREIGN KEY(entity_id) REFERENCES authuser_entities(id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE authuser_entitypermissionuser DROP CONSTRAINT authuser_entitypermi_entity_id_0098dda2_fk_authuser_;
ALTER TABLE authuser_entitypermissiongroup ADD CONSTRAINT entiteta_omejitev_epu FOREIGN KEY(entity_id) REFERENCES authuser_entities(id) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER //
CREATE TRIGGER ADD_ENTITY_TRIGGER
AFTER INSERT ON authuser_entities
FOR EACH ROW
BEGIN
    DECLARE eid VARCHAR(12);
    DECLARE et VARCHAR(12);

    SET eid := NEW.id;
    SET et := (SELECT entity_type_id FROM authuser_entities WHERE id = eid);

    IF et = 'et1' THEN
  	    INSERT INTO authuser_entitypermissiongroup (group_id, entity_id, value) VALUES
        ('g0', eid, 49),
        ('g1', eid, 1);
    ELSEIF et IN('et2', 'et3', 'et5') THEN
  	    INSERT INTO authuser_entitypermissiongroup (group_id, entity_id, value) VALUES
        ('g0', eid, 1);
    END IF;
END;//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CASCADE_DELETE_USER1(IN uid VARCHAR(12))
BEGIN
    DECLARE eid VARCHAR(12);
    DECLARE done BOOL DEFAULT FALSE;

    DECLARE c1 CURSOR FOR SELECT id FROM authuser_entities WHERE owner_id = uid;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    SET done = FALSE;
    OPEN c1;
    read_loop: LOOP
        FETCH c1 INTO eid;
        IF done THEN
            LEAVE read_loop;
        END IF;
        DELETE FROM authuser_entitypermissiongroup WHERE entity_id = eid;
		DELETE FROM authuser_entitypermissionuser WHERE entity_id = eid;
	END LOOP;
    CLOSE c1;
    DELETE FROM authuser_entities WHERE owner_id = uid;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CASCADE_DELETE_USER2(IN uid VARCHAR(12))
BEGIN
    DECLARE gid VARCHAR(12);
    DECLARE done BOOL DEFAULT FALSE;

    DECLARE c1 CURSOR FOR SELECT id FROM authuser_group WHERE owner_id = uid;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    SET done = FALSE;
    OPEN c1;
    read_loop: LOOP
        FETCH c1 INTO gid;
        IF done THEN
            LEAVE read_loop;
        END IF;
        DELETE FROM authuser_entitypermissiongroup WHERE group_id = gid;
        DELETE FROM authuser_group_user WHERE group_id = gid;
		DELETE FROM authuser_group WHERE id = gid;
	END LOOP;
    CLOSE c1;
    DELETE FROM authuser_group WHERE owner_id = uid;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CASCADE_DELETE_USER(IN uid VARCHAR(12))
BEGIN
	DELETE FROM authuser_group_user WHERE user_id = uid;
    DELETE FROM authuser_entitypermissionuser WHERE user_id = uid;
    CALL CASCADE_DELETE_USER1(uid);
    CALL CASCADE_DELETE_USER2(uid);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER REMOVE_USER_TRIGGER
BEFORE DELETE ON authuser_user
FOR EACH ROW
BEGIN
	DECLARE uid VARCHAR(12);
    SET uid := OLD.uid;-- (SELECT id FROM authuser_user WHERE user_id = OLD.id LIMIT 1);
    CALL CASCADE_DELETE_USER(uid);
    -- DELETE FROM authuser_user WHERE id = uid;
END;//
DELIMITER ;


DELIMITER //
CREATE TRIGGER REMOVE_GROUP_TRIGGER
BEFORE DELETE ON authuser_group
FOR EACH ROW
BEGIN
	DECLARE gid VARCHAR(12);
    SET gid := OLD.id;
    DELETE FROM authuser_group_user WHERE group_id = gid;
    DELETE FROM authuser_entitypermissiongroup WHERE group_id = gid;
END;//
DELIMITER ;