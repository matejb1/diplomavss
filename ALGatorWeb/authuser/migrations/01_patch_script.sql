USE algator;

ALTER TABLE authuser_user DROP FOREIGN KEY authuser_user_user_id_8be030c8_fk_auth_user_id;
ALTER TABLE authuser_entities CHANGE COLUMN is_private is_private BOOL NOT NULL DEFAULT TRUE;

DELIMITER //
CREATE TRIGGER ADD_ENTITY_TRIGGER
AFTER INSERT ON authuser_entities
FOR EACH ROW
BEGIN
    DECLARE eid INTEGER;
    DECLARE et INTEGER;

    SET @eid := NEW.id;
    SET @et := (SELECT entity_type_id FROM authuser_entities WHERE id = @eid);

    IF @et = 'et1' THEN
  	    INSERT INTO authuser_entitypermissiongroup (group_id, entity_id, value) VALUES
        ('g0', @eid, 49),
        ('g1', @eid, 1);
    ELSEIF @et IN('et2', 'et3', 'et5') THEN
  	    INSERT INTO authuser_entitypermissiongroup (group_id, entity_id, value) VALUES
        ('g0', @eid, 1);
    END IF;
END;//
DELIMITER ;


DELIMITER //
CREATE TRIGGER ADD_USER_TRIGGER
AFTER INSERT ON auth_user
FOR EACH ROW
BEGIN
	DECLARE uid INTEGER;
    SET uid := NEW.id;
    INSERT INTO authuser_user (id, user_id) VALUES (CONCAT('u',uid-1), uid);
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
BEFORE DELETE ON auth_user
FOR EACH ROW
BEGIN
	DECLARE uid VARCHAR(12);
    SET uid := (SELECT id FROM authuser_user WHERE user_id = OLD.id LIMIT 1);
    CALL CASCADE_DELETE_USER(uid);
    DELETE FROM authuser_user WHERE id = uid;
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