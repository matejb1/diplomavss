import json

from MySQLdb import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from authuser.models import User, Group, Group_User, EntityPermissionUser, PermissionType, Entities, \
    EntityPermissionGroup, Entity_permission, EntityType
from authuser.helper import is_null_or_empty, is_valid_id, run_query, contains
from Classes.GlobalConfig import globalConfig
from authuser.queries import PERMISSIONS_ENTTIES_USER_GROUP_ROOT, PERMISSIONS_ENTTIES_USER_GROUP


def get_next_group_id() -> str:
    """This function will return next available group id.

    Returns:
        str: Next available group id
    """
    try:
        return f"g{int(Group.objects.latest('id').id[1:]) + 1}"
    except ObjectDoesNotExist:
        return "g0"
    except Exception:
        raise ValueError("Cannot get next group id.")


def get_next_entity_id() -> str:
    """This function will return next available entity id.

    Returns:
        str: Next available entity id.
    """
    try:
        return f"e{int(Entities.objects.latest('id').id[1:]) + 1}"
    except ObjectDoesNotExist:
        return "e0"
    except Exception:
        raise ValueError("Cannot get next entity id.")

# TODO: Check if user has permission to add group --> can(owner, ?, ?)
def add_group(owner: str, group_name: str):
    """This function will create group if the user has permission to create it and if group name is unique in database.

    Args:
        owner (str): uid of user
        group_name (str): unique group name
    """
    gid = get_next_group_id()
    if is_null_or_empty(owner) or is_null_or_empty(gid) or is_null_or_empty(group_name) or not is_valid_id('u', owner):
        globalConfig.logger.error(
            "ERROR: authuser.repository#add_group: At least one data is NULL (owner, group_name).")
        raise ValueError("ERROR: authuser.repository#add_group: At least one data is NULL (owner, group_name).")

    try:
        user = User.objects.get(uid=owner.strip())
        group_name = group_name.strip()
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.get_or_create(id=gid, name=group_name, owner=user)
            globalConfig.logger.info("INFO: authuser.repository#add_group: Added group successfully.")
        else:
            globalConfig.logger.warning("WARNING: authuser.repository#add_group: Group already exists.")
    except ObjectDoesNotExist as e:
        globalConfig.logger.error("ERROR: authuser.repository#add_group: User doesn't exists.")
    except Exception as e:
        globalConfig.logger.error("ERROR: authuser.repository#add_group: Exception occurred.")


def add_user(username: str, email: str, password: str):
    """This function can create new user to database.

    Args:
        username (str): username of new user
        email (str): email of new user
        password (str): password of new user
    """
    if is_null_or_empty(username) or is_null_or_empty(email) or is_null_or_empty(password):
        globalConfig.logger.error("ERROR: authuser.repository#add_user: At least one data is NULL (owner, group_name).")
        raise ValueError("ERROR: authuser.repository#add_user: At least one data is NULL (owner, group_name).")
    try:
        User.objects.create_user(username.strip(), email.strip(), password.strip())
        globalConfig.logger.info("INFO: authuser.repository#add_user: Created user successfully.")
    except IntegrityError:
        globalConfig.logger.warning("WARNING: authuser.repository#add_user: User already exists, skipping.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#add_user: Exception occurred.")


def add_user_to_group(username: str, gid: str):
    """This function can add user to existing group.

    Args:
        username (str): Which user should be added to following group.
        gid (str): Group id.
    """
    if is_null_or_empty(username) or is_null_or_empty(gid):
        globalConfig.logger.error("ERROR: authuser.repository#add_user_to_group: At least one data is NULL (username, "
                                  "gid).")
        raise ValueError("ERROR: authuser.repository#add_user_to_group: At least one data is NULL (username, gid).")

    try:
        user = User.objects.get(username=username.strip())
        group = Group.objects.get(pk=gid.strip())

        if not Group_User.objects.filter(user=user, group=group).exists():
            Group_User.objects.get_or_create(user=user, group=group)
            globalConfig.logger.info("INFO: authuser.repository#add_user_to_group: User has been added to group "
                                     "successfully.")
        else:
            globalConfig.logger.warning("WARNING: authuser.repository#add_user_to_group: User is already in the group.")
    except ObjectDoesNotExist:
        globalConfig.logger.error("ERROR: authuser.repository#add_user_to_group: User or group doesn't exists in "
                                  "database.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#add_user_to_group: Exception occurred.")


def edit_user(id: int, username: str, email: str, is_superuser: bool = False, is_staff: bool = False,
              is_active: bool = True):
    """This function will modify the user.

    Args:
        id (id): user id (table id)
        username (str): new username of existing user
        email (str): new mail of existing user
        is_superuser (bool): is superuser
        is_staff (bool): is staff
        is_active (bool): is active
    """
    if not User.objects.filter(id=id).exists() or is_null_or_empty(username) or is_null_or_empty(email):
        globalConfig.logger.error(
            "ERROR: authuser.repository#edit_user: At least one data is NULL (id, username, mail)")
        raise ValueError("ERROR: authuser.repository#edit_user: At least one data is NULL (id, username, mail)")

    try:
        uid = User.objects.get(pk=id)
        if User.objects.filter(username=username).exists() and User.objects.get(username=username).pk != id:
            raise ValueError("ERROR: authuser.repository#edit_user: Username already in user by other user.")
        uid.username = username.strip()
        uid.email = email.strip()
        uid.is_superuser = is_superuser
        uid.is_staff = is_staff
        uid.is_active = is_active
        uid.save()
        globalConfig.logger.info("INFO: authuser.repository#edit_user: Successfully updated user.")
    except ObjectDoesNotExist:
        globalConfig.logger.error(f"ERROR: authuser.repository#edit_user: User with following id: {id} doesn't exists.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#edit_user: Exception occurred.")


def remove_group(group_id: str):
    """This function will permanently delete the group from database.

    Args:
        group_id (str): group id
    """
    if is_null_or_empty(group_id) or not is_valid_id('g', group_id):
        globalConfig.logger.error("ERROR: authuser.repository#remove_group: cannot remove empty or None group.")
        raise ValueError("ERROR: authuser.repository#remove_group: cannot remove empty or None group.")

    try:
        if Group.objects.filter(pk=group_id).exists():
            Group.objects.get(pk=group_id).delete()
            globalConfig.logger.info("INFO: authuser.repository#remove_group: Successfully deleted group.")
        else:
            globalConfig.logger.warning("WARNING: authuser.repository#remove_group: Group doesn't exists.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#remove_group: Exception occurred")


def remove_user(uid: str):
    """This function will permanently delete the user from database.

    Args:
        uid (str): user identifier
    """
    if is_null_or_empty(uid) or not is_valid_id('u', uid):
        globalConfig.logger.error("ERROR: authuser.repository#add_user_to_group: uid cannot be empty.")
        raise ValueError("ERROR: authuser.repository#add_user_to_group: uid cannot be empty.")

    try:
        run_query("DELETE FROM authuser_user WHERE uid = %s", [uid])
        globalConfig.logger.info("INFO: authuser.repository#remove_user: Removing the user was successful.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#remove_user: Exception occurred.")


def remove_user_from_group(username: str, gid: str):
    """This function will delete the user from group.

    Args:
        username (str): username of user
        gid (str): group id
    """
    if is_null_or_empty(username) or is_null_or_empty(gid) or not is_valid_id('g', gid):
        globalConfig.logger.error(
            "ERROR: authuser.repository#remove_user_from_group: username or gid is None or not valid.")
        raise ValueError("ERROR: authuser.repository#remove_user_from_group: username or gid is None or not valid.")

    try:
        uid = User.objects.get(username=username)
        gid = Group.objects.get(pk=gid)
        Group_User.objects.get(user=uid, group=gid).delete()
        globalConfig.logger.info(
            "INFO: authuser.repository#remove_user_from_group: Removing user from group was successfull.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#remove_user_from_group: Exception occurred.")


def add_permission_to_user(username: str, codename: str, entity_id: str):
    """This function will add permission on entity.

    Args:
        username (str): username of user
        codename (str): permission
        entity_id (str): entity
    """
    if is_null_or_empty(username) or is_null_or_empty(codename) or is_null_or_empty(entity_id):
        globalConfig.logger.error(
            "ERROR: authuser.repository#add_permission_to_user: username, permission or entity id is empty.")
        raise ValueError(
            "ERROR: authuser.repository#add_permission_to_user: username, permission or entity id is empty.")
    try:
        pid = PermissionType.objects.get(codename=codename)
        eid = Entities.objects.get(pk=entity_id)
        user = User.objects.get(username=username)

        epu, created = EntityPermissionUser.objects.get_or_create(entity=eid, user=user)

        if not created and not contains(epu.value, pid.value):
            epu.value |= pid.value
            epu.save()
        elif created:
            epu.value = pid.value
            epu.save()
        globalConfig.logger.info("INFO: authuser.repository#add_permission_to_user: Updated permission for user.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#add_permission_to_user: Exception occurred.")


def add_permission_to_group(group_id: str, codename: str, entity_id: str):
    """This function will add permission on entity.

    Args:
        group_id (str): group id
        codename (str): permission
        entity_id (str): entity
    """
    if is_null_or_empty(group_id) or is_null_or_empty(codename) or is_null_or_empty(entity_id):
        globalConfig.logger.error(
            "ERROR: authuser.repository#add_permission_to_user: group id, permission or entity id is empty.")
        raise ValueError(
            "ERROR: authuser.repository#add_permission_to_user: group id, permission or entity id is empty.")
    try:
        pid = PermissionType.objects.get(codename=codename)
        eid = Entities.objects.get(pk=entity_id)
        gid = Group.objects.get(pk=group_id)

        epg, created = EntityPermissionGroup.objects.get_or_create(entity=eid, group=gid)

        if not created and not contains(epg.value, pid.value):
            epg.value |= pid.value
            epg.save()
        elif created:
            epg.value = pid.value
            epg.save()
        globalConfig.logger.info("INFO: authuser.repository#add_permission_to_group: Updated permission for group.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#add_permission_to_group: Exception occurred.")


def update_user_permission(user_id: str, permission_id: str, entity_id: str, value: int):
    """This function will update permission on entity.

    Args:
        user_id (str): user id
        permission_id (str): permission
        entity_id (str): entity
        value(int): value
    """
    if is_null_or_empty(user_id) or is_null_or_empty(permission_id) or is_null_or_empty(entity_id) or not is_valid_id(
            'u', user_id):
        globalConfig.logger.error(
            "ERROR: authuser.repository#update_user_permission: user id, permission or entity id is empty.")
        raise ValueError(
            "ERROR: authuser.repository#update_user_permission: user id, permission or entity id is empty.")

    try:
        uid = User.objects.get(uid=user_id)
        pid = PermissionType.objects.get(pk=permission_id)
        eid = Entities.objects.get(pk=entity_id)
        epu = EntityPermissionUser.objects.get(user=uid, entity=eid)

        if pid.value == value:
            epu.value &= ~value
            epu.save()
            globalConfig.logger.info("INFO: authuser.repository#update_user_permission: Updated permission for user.")
        else:
            raise Exception()
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#update_user_permission: Exception occurred.")


def update_group_permission(group_id: str, permission_id: str, entity_id: str, value: int):
    """This function will update permission on entity.

    Args:
        group_id (str): group id
        permission_id (str): permission
        entity_id (str): entity
        value(int): value
    """
    if is_null_or_empty(group_id) or is_null_or_empty(permission_id) or is_null_or_empty(entity_id) or not is_valid_id(
            'g', group_id):
        globalConfig.logger.error(
            "ERROR: authuser.repository#update_group_permission: group id, permission or entity id is empty.")
        raise ValueError(
            "ERROR: authuser.repository#update_group_permission: group id, permission or entity id is empty.")

    try:
        gid = Group.objects.get(pk=group_id)
        pid = PermissionType.objects.get(pk=permission_id)
        eid = Entities.objects.get(pk=entity_id)
        epg = EntityPermissionGroup.objects.get(group=gid, entity=eid)

        if pid.value == value:
            epg.value &= ~value
            epg.save()
            globalConfig.logger.info("INFO: authuser.repository#update_group_permission: Updated permission for group.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#update_group_permission: Exception occurred.")


def get_entities(uid: str) -> list:
    """This function will get entties related to user.

    Args:
        uid (str): user id

    Returns:
        list: entities
    """
    if is_null_or_empty(uid) or not is_valid_id('u', uid):
        globalConfig.logger.error("ERROR: authuser.repository#get_entities: uid is None or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#get_entities: uid is None or empty or isn't valid.")

    data = []
    try:
        user = User.objects.get(uid=uid)
        if uid == 'u0':
            data = Entities.objects.all()
            globalConfig.logger.info("INFO: authuser.repository#get_entities: Fetched all entties.")
        elif uid != 'u1':
            data.extend(Entities.objects.filter(owner=user))
            for gu in Group_User.objects.filter(user=user):
                for epg in EntityPermissionGroup.objects.filter(group=gu.group):
                    if epg.entity not in data:
                        data.append(epg.entity)

            for epu in EntityPermissionUser.objects.filter(user=user):
                if epu.entity not in data:
                    data.append(epu.entity)
            globalConfig.logger.info("INFO: authuser.repository#get_entities: Fetched entties related to user.")
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#get_entities: Exception occurred.")
    return data


def get_groups_user(uid: str) -> list:
    """This function will get all groups where specific user belongs.

    Args:
        uid (str): user id

    Returns:
        list: groups where user belongs
    """
    if is_null_or_empty(uid) or not is_valid_id('u', uid):
        globalConfig.logger.error("ERROR: authuser.repository#get_groups_user: uid is None or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#get_groups_user: uid is None or empty or isn't valid.")
    data = []
    try:
        user = User.objects.get(uid=uid)
        if uid == 'u0':  # root
            data = Group.objects.all()
        elif uid != 'u1':
            data = [gu.group for gu in Group_User.objects.filter(user=user)]
            data.extend(Group.objects.filter(owner=user))
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#get_entities: Exception occurred.")
    return data


def get_groups(uid: str, entity_id: str) -> list:
    """This function returns all groups, where user belongs and has write permission on entity.

    Args:
        uid (str): user id
        entity_id (str): entity id

    Returns:
        list: groups
    """
    if is_null_or_empty(uid) or is_null_or_empty(entity_id) or not is_valid_id('u', uid) or not is_valid_id('e',
                                                                                                            entity_id):
        globalConfig.logger.error("ERROR: authuser.repository#get_groups: uid or eid is None or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#get_groups: uid or eid is None or empty or isn't valid.")

    data = []
    user = None
    eid = None
    pw = None
    try:
        user = User.objects.get(uid=uid)
        eid = Entities.objects.get(pk=entity_id)
        pw = PermissionType.objects.get(codename='can_write').value
    except Exception:
        raise ValueError("ERROR: authuser.repository#get_groups: user or entty doesn't exists.")

    if uid == 'u0':
        data.extend(Group.objects.all())
    elif uid != 'u1':
        for gu in Group_User.objects.filter(user=user):
            try:
                epg = EntityPermissionGroup.objects.get(group=gu.group, entity=eid)
                if contains(epg.value, pw):
                    data.append(gu.group)
            except Exception:
                continue
        data.extend(Group.objects.filter(owner=user))
    return data


def get_all_user_permissions_by_eid(eid: str) -> list:
    """This function gets all possible permission types for specific entity.

    Args:
        eid (str): entity id

    Returns:
        list: permission types of one entity
    """
    if is_null_or_empty(eid) or not is_valid_id('e', eid):
        globalConfig.logger.error(
            "ERROR: authuser.repository#get_all_user_permissions_by_eid: eid is None or empty or isn't valid.")
        raise ValueError(
            "ERROR: authuser.repository#get_all_user_permissions_by_eid: eid is None or empty or isn't valid.")

    et = Entities.objects.get(pk=eid).entity_type
    ep = Entity_permission.objects.filter(entity_type=et)
    return [p.permission_type for p in ep]


def entities_permissions(uid: str) -> list:
    """This function returns rights has user and groups, where it belongs to.

    Args:
        uid (str): user id

    Returns:
        list: which rights has user and groups, where it belongs to.
    """
    if is_null_or_empty(uid) or not is_valid_id('u', uid):
        globalConfig.logger.error(
            "ERROR: authuser.repository#entities_permissions: uid is None or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#entities_permissions: uid is None or empty or isn't valid.")
    data = []
    try:
        if uid == 'u0':
            data = run_query(PERMISSIONS_ENTTIES_USER_GROUP_ROOT, [])
        else:
            data = run_query(PERMISSIONS_ENTTIES_USER_GROUP, [uid, uid])
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#entities_permissions: Exception occurred")
    return data


def add_entity(uid: str, name: str, et: str, parent: str, is_private: bool = True):
    """This function will insert entity into a database.

    Args:
        uid (str): Owner of entity.
        name (str): Name of entity.
        et (str): Entity type id.
        parent (str): Parent
        is_private (bool): Is entity private. Default True.
    """
    if (is_null_or_empty(uid) or is_null_or_empty(name) or is_null_or_empty(et) or
            not (is_valid_id('u', uid) and is_valid_id('et', et))):
        globalConfig.logger.error("ERROR: authuser.repository#add_entity: uid, name, entity typpe or parent is None "
                                  "or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#add_entity: uid, name, entity typpe or parent is None or empty "
                         "or isn't valid.")

    try:
        new_id = get_next_entity_id()
        et = EntityType.objects.get(pk=et)
        user = User.objects.get(uid=uid)
        parent_obj = None

        if not is_null_or_empty(parent) and is_valid_id('u', parent):
            parent_obj = Entities.objects.get(pk=parent)

        Entities.objects.create(id=new_id,
                                name=name,
                                entity_type=et,
                                owner=user,
                                parent=parent_obj,
                                is_private=is_private)
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#add_entity: Exception occurred")


def remove_entity(eid: str):
    """This function will permanently delete entity from database.

    Args:
        eid (str): entity id
    """
    if is_null_or_empty(eid) or is_valid_id('e', eid):
        globalConfig.logger.error("ERROR: authuser.repository#remove_entity: eid is None or empty or isn't valid.")
        raise ValueError("ERROR: authuser.repository#remove_entity: eid is None or empty or isn't valid.")
    try:
        Entities.objects.get(pk=eid).delete()
    except Exception:
        globalConfig.logger.error("ERROR: authuser.repository#remove_entity: Exception occurred")


def can(uid: str, eid: str, codename: str) -> bool:
    """This function returns True or False depending on, if user has permission on specific entity.

    Args:
        uid (str): user id
        eid (str): entity id
        codename (str): code name

    Returns:
        bool: Returns True if user has permission on specific entity.
    """
    if (is_null_or_empty(uid) or is_null_or_empty(eid) or is_null_or_empty(codename)) or not (
            is_valid_id('u', uid) and is_valid_id('e', eid)):
        raise ValueError("ERROR: Can(uid, eid, codename) at least one parameter is empty or Null or invalid.")

    try:
        if uid == 'u0':  # Root
            return True
        e = Entities.objects.get(pk=eid)
        if e.owner.uid == uid:  # Owner
            return True
        if e.is_private:  # Entity is private
            return False
        user = User.objects.get(uid=uid)
        p = PermissionType.objects.get(codename=codename)
        pfc = PermissionType.objects.get(codename='full_control')
        try:
            epu = EntityPermissionUser.objects.get(entity=e, user=user)
            if contains(epu.value, p.value, pfc.value):
                return True
        except EntityPermissionUser.DoesNotExist:
            pass
        groups = [gu.group for gu in Group_User.objects.filter(user=user)]
        groups.append(Group.objects.get(pk=('g1' if uid == 'u1' else 'g0')))
        for g in groups:
            try:
                epg = EntityPermissionGroup.objects.get(entity=e, group=g)
                if contains(epg.value, p.value, pfc.value):
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False