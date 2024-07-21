import json

from django.core import serializers
from django.http import QueryDict, HttpResponse

from .helper import contains, try_get_user, is_null_or_empty, is_valid_id
from .models import Group, PermissionType, EntityPermissionUser, Entities, EntityPermissionGroup, Group_User, \
    User

import authuser.repository as repository
from authuser.repository import can


def add_group(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_group, and it returns the status of adding.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains name of the group.

    Returns:
        HttpResponse: Status of adding new group to database.
    """
    if response is None or not data or "name" not in data:
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_rights'):
            repository.add_group(uid, data['name'].strip())
            response.status_code = 201
            response.content = {"Success": "User exists in this group."}
        else:
            raise Exception()
    except Exception:
        response.status_code = 500
        response.content = {"Error": "ERROR: Exception occurred at adding new group."}
    return response


def add_user(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_user, and it returns the status of adding.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains information about the user (username, email, password).

    Returns:
        HttpResponse: Status of adding new user to database.
    """
    if response is None or not data or not ("username" in data and "email" in data and "password" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)

    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            repository.add_user(data['username'].strip(), data['email'].strip(), data['password'].strip())
            response.status_code = 201
            response.content = {"Info": "Successfully added new user."}
        else:
            raise Exception()
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot create user."}
    return response


def get_all_permission_types(request: HttpResponse) -> HttpResponse:
    """This function gets all permission types and it returns them.

    Args:
        request (HttpResponse): Status to be applied to response of requested action.

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if request is None:
        return HttpResponse({"Error": "ERROR: Response is None."}, status=500)
    response = HttpResponse()
    response.content_type = "application/json"
    try:
        response.content = serializers.serialize("json", PermissionType.objects.all(), )
        response.status_code = 200
    except Exception:
        response.content = {"Error": "Cannot get all permission types."}
        response.status_code = 500
    return response


def add_user_to_group(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_user_to_group, and it returns the status of adding.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains information about user and group.

    Returns:
        HttpResponse: Status of adding user to group.
    """
    if response is None or not data or not ("username" in data and "gid" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            repository.add_user_to_group(data["username"].strip(), data["gid"].strip())
            response.status_code = 201
            response.content = {"Info": "Successfully added user to group."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot add user to group."}
    return response


def edit_user(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function edit_user, and returns status of editing.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains information about user.

    Returns:
        HttpResponse: Status if user was edited successfully.
    """
    if response is None or not data or not ("id" in data and "username" in data and "email" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        is_superuser = False
        is_staff = False
        is_active = False

        if "isSuperUser" in data:
            is_superuser = data['isSuperUser'].strip() == 'true'
        if "isStaff" in data:
            is_staff = data['isStaff'].strip() == 'true'
        if "isActive" in data:
            is_active = data['isActive'].strip() == 'true'

        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            repository.edit_user(int(data['id'].strip()),
                                 data['username'].strip(),
                                 data['email'].strip(),
                                 is_superuser,
                                 is_staff,
                                 is_active)
            response.status_code = 202
            response.content = {"Info": "User has been modified."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot modify user."}
    return response


def remove_group(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function remove_group, and returns status of removing the group.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains group_id.

    Returns:
        HttpResponse: Status if group was deleted successfully.
    """
    if response is None or not data or "group_id" not in data:
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        u = try_get_user(response)
        if can(u, 'e0', 'can_edit_users'):
            repository.remove_group(data['group_id'].strip())
            response.status_code = 203
            response.content = {"Info": "Group has been deleted successfully."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response


def remove_user(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function remove_user, and returns status of removing.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains uid.

    Returns:
        HttpResponse:Status if user was deleted successfully.
    """
    if response is None or not data or "uid" not in data:
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)

    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            repository.remove_user(data['uid'])
            response.status_code = 203
            response.content = {"Info": "User was successfully deleted."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response


def remove_user_from_group(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function remove_user_from_group, and returns status of removing.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains username and group id.

    Returns:
        HttpResponse: Status if user was removed from group successfully.
    """
    if response is None or not ("username" in data and "gid" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            repository.remove_user_from_group(data["username"], data["gid"])
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response


def add_permission_to_user(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_permission_to_user, and returns status of applying.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains username, permission and entity id.

    Returns:
        HttpResponse: Status if permission for user was added successfully.

    """
    if response is None or not data or not ("id" in data and "permission_id" in data and "entity_id" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        u = try_get_user(response)
        if can(u, data["entity_id"], data["permission_id"],):
            repository.add_permission_to_user(data["id"], data["permission_id"], data["entity_id"])
            response.status_code = 201
            response.content = {"Info": "Successfully added permission."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Permission has not been added."}
    return response


def add_permission_to_group(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_permission_to_group, and returns status of applying.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains group id, permission and entity id.

    Returns:
        HttpResponse: Status if permission for group was added successfully.

    """
    if response is None or not data or not ("id" in data and "permission_id" in data and "entity_id" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        u = try_get_user(response)
        if can(u, data["entity_id"], data["permission_id"]):
            repository.add_permission_to_group(data["id"], data["permission_id"], data["entity_id"])
            response.status_code = 201
            response.content = {"Info": "Successfully added permission."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Permission has not been added."}
    return response


def update_user_permission(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function update_user_permission, and returns status of applying.

    Args:
        response (HttpResponse):  Status to be applied to response of requested action.
        data (dict): Contains uid, permission and entity id.

    Returns:
        HttpResponse: Status if permission for user was updated successfully.
    """
    response.content_type = "application/json"

    if response is None or not data or not (
            "id" in data and "permission_id" in data and "entity_id" in data and "value" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)

    try:
        u = try_get_user(response)
        if can(u, 'e0', 'can_edit_users'):
            repository.update_user_permission(data["id"], data["permission_id"], data["entity_id"], int(data["value"]))
            response.status_code = 202
            response.content = {"Info": "Successfully updated permission."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "ERROR: Permission has not been updated."}
    return response


def update_group_permission(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function update_group_permission, and returns status of applying.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains gid, permission and entity id.

    Returns:
        HttpResponse: Status if permission for group was updated successfully.
    """

    if response is None or not data or not (
            "id" in data and "permission_id" in data and "entity_id" in data and "value" in data):
        return HttpResponse({"Error": "ERROR: Response is None or no data is present."}, status=500)
    response.content_type = "application/json"
    try:
        u = try_get_user(response)
        if can(u, 'e0', 'can_edit_users'):
            repository.update_group_permission(data["id"], data["permission_id"], data["entity_id"], int(data["value"]))
            response.status_code = 202
            response.content = {"Info": "Successfully updated permission."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "ERROR: Permission has not been updated."}
    return response


def get_entities(request: HttpResponse, *args) -> HttpResponse:
    """This function passes data to repository function get_entities, and returns entties.

    Args:
        request (HttpResponse): Data to be applied on response object.
        *args ():

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if request is None:
        return HttpResponse({"Error": "ERROR: Request is None."}, status=500)
    response = HttpResponse()
    response.content_type = "application/json"
    try:
        uid = try_get_user(request)
        if can(uid, 'e0', 'can_edit_rights'):
            data = repository.get_entities(uid)
            response.content = serializers.serialize("json", data, )
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "ERROR: cannot get entties."}
    return response


def get_users(response: HttpResponse, *args) -> HttpResponse:
    """This function returns users.

    Args:
        response (HttpResponse): Data to be applied on response object.
        *args ():

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if response is None:
        return HttpResponse({"Error": "ERROR: Request is None."}, status=500)
    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            data = User.objects.all()
            users = serializers.serialize("json", data, fields=["username", "email", "is_superuser"])
            response.content = users
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.content = {"Error": "ERROR: cannot get users."}
        response.status_code = 500
    return response


def get_user(response: HttpResponse, id: int) -> HttpResponse:
    """This function returns specific user.

    Args:
        response (HttpResponse): Data to be applied on response object.
        id (int): id of user

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if response is None:
        return HttpResponse({"Error": "ERROR: Request is None."}, status=500)

    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_users'):
            data = User.objects.get(pk=id)
            response.status_code = 200
            response.content = serializers.serialize('json', [data, ],
                                                     fields=["username", "email", "is_superuser", "is_staff",
                                                             "is_active"])
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.content = {"Error": "ERROR: cannot get user."}
        response.status_code = 500
    return response


def get_groups_user(request: HttpResponse, *args) -> HttpResponse:
    """This function passes data to repository function get_groups_user and returns all groups, where user belongs.

    Args:
        request (HttpResponse): Data to be applied on response object.
        *args ():

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if request is None:
        return HttpResponse({"Error": "ERROR: Request is None."}, status=500)

    response = HttpResponse()
    response.content_type = "application/json"
    try:
        uid = try_get_user(request)
        if can(uid, 'e0', 'can_edit_rights'):
            data = repository.get_groups_user(uid)
            response.content = serializers.serialize("json", list(set(data)), )
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot get groups."}
    return response


def get_groups(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function get_groups and returns all groups, where user belongs and has write permission on entity.

    Args:
        response (HttpResponse): Data to be applied on response object.
        data (dict): Contains eid.

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if response is None or not data or "eid" not in data:
        return HttpResponse({"Error": "ERROR: Request is None or data isn't present."}, status=500)

    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        if can(uid, 'e0', 'can_edit_rights'):
            groups = repository.get_groups(uid, data["eid"])
            response.content = serializers.serialize("json", list(set(groups)), )
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot get groups."}
    return response


def get_all_user_permissions_by_eid(request: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository funciton get_all_user_permissions_by_eid, and returns all possible permission types for specific entity.

    Args:
        request (HttpResponse): Data to be applied on response object.
        data (dict): Contains eid.

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if request is None or not data or "eid" not in data:
        return HttpResponse({"Error": "ERROR: Request is None or data isn't present."}, status=500)

    response = HttpResponse()
    response.content_type = "application/json"
    try:
        uid = try_get_user(request)
        if can(uid, 'e0', 'can_edit_rights'):
            data = repository.get_all_user_permissions_by_eid(data['eid'])
            response.content = serializers.serialize("json", data, )
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot get permissions."}
    return response


def entities_permissions(request: HttpResponse, *args) -> HttpResponse:
    """This function passes data to repository function entities_permissions and returns rights has user and groups, where it belongs to.

    Args:
        request (HttpResponse):  Data to be applied on response object
        *args ():

    Returns:
        HttpResponse: Serialized JSON response.
    """
    if request is None:
        return HttpResponse({"Error": "ERROR: Request is None."}, status=500)
    response = HttpResponse()
    response.content_type = "application/json"
    try:
        uid = try_get_user(request)
        if can(uid, 'e0', 'can_edit_rights'):
            response.content = json.dumps(repository.entities_permissions(uid))
            response.status_code = 200
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot get permissions."}
    return response


def add_entity(response: HttpResponse, data: dict) -> HttpResponse:
    """This function passes data to repository function add_entity and insert entity into a database.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains uid, name, et. Optionally parent and is_private.

    Returns:
        HttpResponse: Status of adding new entity to database.
    """
    if response is None or not data or not ("et" in data and "uid" in data and "name" in data):
        return HttpResponse({"Error": "ERROR: Response is None or data isn't present."}, status=500)

    response.content_type = "application/json"
    try:
        uid1 = try_get_user(response)  # User who send
        uid = data['uid']  # For user, we're asking
        name = data["name"]
        et = data['et']
        is_private = True
        parent = None

        if 'is_private' in data and data['is_private'] in ['true', 'false']:
            is_private = data['is_private'] == 'true'

        if 'parent' in data:
            parent = data['parent']

        can1 = can(uid, 'e0', 'can_edit_rights')
        if (uid == uid1 and can1) or (uid != uid1 and can1 and can(uid1, 'e0', 'can_edit_rights')):
            repository.add_entity(uid, name, et, parent, is_private)
            response.status_code = 201
            response.content = {"Info": "Successfully added entity."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot add entity."}
    return response


def remove_entity(response: HttpResponse, data: dict) -> HttpResponse:
    """This function pass data to repository function remove_entity, and it will permanently delete entity from database.

    Args:
        response (HttpResponse): Status to be applied to response of requested action.
        data (dict): Contains entity id - eid.

    Returns:
        HttpResponse: Status of removing entity.
    """
    if response is None or not data or "eid" not in data:
        return HttpResponse({"Error": "ERROR: Response is None or data isn't present."}, status=500)

    response.content_type = "application/json"
    try:
        uid = try_get_user(response)
        eid = data['eid']
        if can(uid, eid, 'can_edit_rights'):
            repository.remove_entity(eid)
            response.status_code = 203
            response.content = {"Info": "Successfully removed entity."}
        else:
            raise ValueError("User has no permission to modify other users.")
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot remove entity."}
    return response


def can_request(request: HttpResponse) -> HttpResponse:
    if request is None:
        return HttpResponse({"Error": "ERROR: Response is None."}, status=500)

    data = QueryDict.dict(request.POST)
    if not data or not ("eid" in data and "codename" in data):
        return HttpResponse({"Error": "ERROR: Data isn't present."}, status=500)

    response = HttpResponse()
    try:
        uid = 'u1'
        eid = data["eid"]
        codename = data["codename"]

        if "uid" in data:
            uid = data["uid"]
        else:
            uid = try_get_user(request)

        response.content = can(uid, eid, codename)
    except Exception:
        response.content = False
    return response



