import json

from django.contrib.auth.models import User
from django.core import serializers

from .helper import run_query
from .models import Group, PermissionType, EntityPermissionUser, Entities, EntityPermissionGroup
from .queries import *


def get_single_user_data_view(id):
    data = {}
    user = User.objects.get(pk=int(id))
    data["userdata"] = serializers.serialize("json", [user])
    data["all_groups"] = json.dumps(list(Group.objects.all().values()))
    data["groups"] = json.dumps(list(Group.objects.filter(user=user).values()))
    data["all_permissions"] = json.dumps(list(PermissionType.objects.all().values()))
    data["permissions"] = json.dumps(run_query(PERMISSIONS_ENTTIES_BY_USER, [user.id]))
    data["all_entties"] = json.dumps(run_query(ENTTITES_AND_OWNER))
    return data

def get_single_group_data_view(id):
    data = {}
    group = Group.objects.get(pk=int(id))
    data["group"] = serializers.serialize("json", [group])
    data["permissions"] = json.dumps(run_query(PERMISSIONS_ENTTIES_BY_GROUP, [group.id]))
    data["all_permissions"] = json.dumps(list(PermissionType.objects.all().values()))
    data["all_entties"] = json.dumps(run_query(ENTTITES_AND_OWNER))
    return data


def add_user_to_group(response, data):
    group_id = int(data["group_id"])
    user_id = int(data["user_id"])
    user_is_in_group = bool(run_query(IS_THIS_USER_ALREADY_IN_GROUP, [group_id, user_id])[0][0])
    if not user_is_in_group:
        current_user = User.objects.get(pk=user_id)
        new_group = Group.objects.get(pk=group_id)
        new_group.user.add(current_user)
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def remove_user_from_group(response, data):
    group_id = int(data["group_id"])
    user_id = int(data["user_id"])
    user_is_in_group = bool(run_query(IS_THIS_USER_ALREADY_IN_GROUP, [group_id, user_id])[0][0])
    if user_is_in_group:
        current_user = User.objects.get(pk=user_id)
        new_group = Group.objects.get(pk=group_id)
        new_group.user.remove(current_user)
        response.status_code = 203
    else:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response


def add_permission_to_user(response, data):
    permission_id = int(data["permission_id"])
    entity_id = int(data["entity_id"])
    user_id = int(data["user_id"])
    user_has_permission = bool(run_query(USER_HAS_THAT_PERMISSION, [user_id, entity_id, permission_id])[0][0])
    if not user_has_permission:
        current_user = User.objects.get(pk=user_id)
        entity = Entities.objects.get(pk=entity_id)
        permission = PermissionType.objects.get(pk=permission_id)
        epu = EntityPermissionUser.objects.create(entity=entity, user=current_user, permission=permission)
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response

def add_permission_to_group(response, data):
    permission_id = int(data["permission_id"])
    entity_id = int(data["entity_id"])
    group_id = int(data["group_id"])
    group_has_permission = bool(run_query(GROUP_HAS_THAT_PERMISSION, [group_id, entity_id, permission_id])[0][0])
    if not group_has_permission:
        current_group = Group.objects.get(pk=group_id)
        entity = Entities.objects.get(pk=entity_id)
        permission = PermissionType.objects.get(pk=permission_id)
        epu = EntityPermissionGroup.objects.create(entity=entity, group=current_group, permission=permission)
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def remove_user_permission(response, data):
    permission_id = int(data["permission_id"])
    user_id = int(data["user_id"])
    entity_id = int(data["entity_id"])
    id = int(data["id"])
    user_has_permission = bool(run_query(USER_HAS_THAT_PERMISSION, [user_id, entity_id, permission_id])[0][0])
    if user_has_permission:
        EntityPermissionUser.objects.get(pk=id).delete()
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response

def remove_group_permission(response, data):
    permission_id = int(data["permission_id"])
    group_id = int(data["group_id"])
    entity_id = int(data["entity_id"])
    id = int(data["id"])
    group_has_permission = bool(run_query(GROUP_HAS_THAT_PERMISSION, [group_id, entity_id, permission_id])[0][0])
    if group_has_permission:
        EntityPermissionGroup.objects.get(pk=id).delete()
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response
