import json

from django.core import serializers
from django.http import QueryDict, HttpResponse

from .helper import run_query, jwt_precheck, contains, try_get_user
from .models import Group, PermissionType, EntityPermissionUser, Entities, EntityPermissionGroup, Group_User, \
    User as Usr, EntityType, Entity_permission
from .queries import *


def add_group(response, data):
    try:
        user = Usr.objects.get(uid=try_get_user(response))
        gid = f"g{int(Group.objects.latest('id').id[1:])+1}"
        Group.objects.get_or_create(id=gid, name=data['name'], owner=user)
        response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response

def add_user(response, data):
    try:
        Usr.objects.create_user(data['username'], data['email'], data['password'])
        response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot create user."}
    return response

def get_all_permission_types(request):
    response = HttpResponse()
    response.content = serializers.serialize("json", PermissionType.objects.all(), )
    response.content_type = "application/json"
    return response

def add_user_to_group(response, data):
    response.content_type = "application/json"
    try:
        uid = Usr.objects.get(username=data["username"])
        gid = Group.objects.get(pk=data["gid"])

        Group_User.objects.get_or_create(user=uid, group=gid)
        response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}

    return response


def edit_user(response, data):
    try:
        uid = Usr.objects.get(pk=data['id'])
        uid.username = data['username']
        uid.email = data['email']
        uid.is_superuser = data['isSuperUser'] == 'true'
        uid.is_staff = data['isStaff'] == 'true'
        uid.is_active = data['isActive'] == 'true'
        uid.save()
        response.status_code = 202
    except Exception:
        response.status_code = 500
        response.content = {"Error": "Cannot modify user."}
    return response

def remove_group(response, data):
    response.content_type = "application/json"
    try:
        u = try_get_user(response)
        if u == 'u1':
            raise Exception
        Group.objects.get(pk=data['group_id']).delete()
        response.status_code = 203
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response

def remove_user(response, data):
    response.content_type = "application/json"
    try:
        if can(try_get_user(response), 'e0', 'can_edit_users'):
            run_query("DELETE FROM authuser_user WHERE uid = %s", [data['uid']])
            response.status_code = 203
        else:
            raise Exception
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response

def remove_user_from_group(response, data):
    response.content_type = "application/json"
    try:
        uid = Usr.objects.get(username=data["username"])
        gid = Group.objects.get(pk=data["gid"])
        Group_User.objects.get(user=uid, group=gid).delete()
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response

def add_permission_to_user(response, data):
    try:
        pid = PermissionType.objects.get(codename=data["permission_id"])
        eid = Entities.objects.get(pk=data["entity_id"])

        u = try_get_user(response)
        if not can(u, eid, 'can_write'):
            raise Exception
        user = Usr.objects.get(username=data["id"])

        epu, created = EntityPermissionUser.objects.get_or_create(entity=eid, user=user)
        response.content_type = "application/json"

        if not created and not contains(epu.value, pid.value):
            epu.value |= pid.value
            epu.save()
            response.status_code = 201
        elif created:
            epu.value = pid.value
            epu.save()
            response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def add_permission_to_group(response, data):
    pid = PermissionType.objects.get(codename=data["permission_id"])
    eid = Entities.objects.get(pk=data["entity_id"])
    gid = Group.objects.get(pk=data["id"])

    epg, created = EntityPermissionGroup.objects.get_or_create(entity=eid, group=gid)

    if not created and not contains(epg.value, pid.value):
        epg.value |= pid.value
        epg.save()
        response.status_code = 201
    elif created:
        epg.value = pid.value
        epg.save()
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def update_user_permission(response, data):
    uid = Usr.objects.get(uid=data["id"])
    value = int(data["value"])
    pid = PermissionType.objects.get(pk=data["permission_id"])
    eid = Entities.objects.get(pk=data["entity_id"])
    epu = EntityPermissionUser.objects.get(user=uid, entity=eid)

    if pid.value == value:
        epu.value &= ~value
        epu.save()
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def update_group_permission(response, data):
    gid = Group.objects.get(pk=data["id"])
    value = int(data["value"])
    pid = PermissionType.objects.get(pk=data["permission_id"])
    eid = Entities.objects.get(pk=data["entity_id"])
    epg = EntityPermissionGroup.objects.get(group=gid, entity=eid)

    if pid.value == value:
        epg.value &= ~value
        epg.save()
        response.status_code = 201
    else:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def get_entities(request, *args):
    try:
        user = Usr.objects.get(uid=try_get_user(request))
        response = HttpResponse()
        data = []
        if user.uid == 'u0':
            data = Entities.objects.all()
        else:
            data.extend(Entities.objects.filter(owner=user))
            for gu in Group_User.objects.filter(user=user):
                for epg in EntityPermissionGroup.objects.filter(group=gu.group):
                    if epg.entity not in data:
                        data.append(epg.entity)

            for epu in EntityPermissionUser.objects.filter(user=user):
                if epu.entity not in data:
                    data.append(epu.entity)
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    response.content = serializers.serialize("json", data, )
    response.content_type = "application/json"
    return response

def get_users(response, *args):
    users = serializers.serialize("json", Usr.objects.all(),
                                  fields=["username", "email", "is_superuser"])
    response.content = users
    response.content_type = "application/json"
    return response


def get_user(response, id):
    user = serializers.serialize('json', [Usr.objects.get(pk=id), ],
                                 fields=["username", "email", "is_superuser", "is_staff", "is_active"])
    response.content = user
    response.content_type = "application/json"
    return response


def get_groups_user(request, *args):
    try:
        user = Usr.objects.get(uid=try_get_user(request))
        response = HttpResponse()
        g = []
        if user.uid == 'u0':  # root
            g = Group.objects.all()
        else:
            g = [gu.group for gu in Group_User.objects.filter(user=user)]
            g.extend(Group.objects.filter(owner=user))
        groups = serializers.serialize("json", list(set(g)), )
        response.status_code = 200
        response.content = groups
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    response.content_type = "application/json"
    return response


def get_groups(response, data):
    eid = Entities.objects.get(pk=data["eid"])
    user = Usr.objects.get(uid=try_get_user(response))
    pw = PermissionType.objects.get(codename='can_write').value
    grp = []

    if user.uid == 'u0':
        grp.extend(Group.objects.all())
    else:
        for gu in Group_User.objects.filter(user=user):
            try:
                epg = EntityPermissionGroup.objects.get(group=gu.group, entity=eid)
                if contains(epg.value, pw):
                    grp.append(gu.group)
            except Exception:
                continue
        grp.extend(Group.objects.filter(owner=user))

    groups = serializers.serialize("json", list(set(grp)), )
    response.content = groups
    response.content_type = "application/json"
    return response


def get_all_user_permissions_by_eid(request, data):
    response = HttpResponse()
    et = Entities.objects.get(pk=data['eid']).entity_type
    ep = Entity_permission.objects.filter(entity_type=et)
    pt = [p.permission_type for p in ep]
    permissions = serializers.serialize("json", pt, )
    response.content = permissions
    response.content_type = "application/json"
    return response

def entities_permissions(request, *args):
    user = Usr.objects.get(uid=try_get_user(request))
    response = HttpResponse()
    # gids = ", ".join(f'"{g.group.pk}"' for g in Group_User.objects.filter(user=u))
    data = []
    if user.uid == 'u0':
        data = json.dumps(run_query(PERMISSIONS_ENTTIES_USER_GROUP_ROOT, []))
    else:
        data = json.dumps(run_query(PERMISSIONS_ENTTIES_USER_GROUP, [user.uid, user.uid]))
    response.content = data
    response.content_type = "application/json"
    return response

def add_entity(response, data):
    try:
        new_id = f"e{int(Entities.objects.latest('id').id[1:]) + 1}"
        et = EntityType.objects.get(pk=data['et'])
        user = Usr.objects.get(uid=data['uid'])
        parent = Entities.objects.get(pk=data['parent'])
        is_private = data['is_private'] == 'true' if 'is_private' in data else True
        Entities.objects.create(id=new_id, name=data["name"], entity_type=et, owner=user, parent=parent, is_private=is_private)
        response.status_code = 201
    except Exception:
        response.status_code = 500
    return response

def remove_entity(response, data):
    try:
        Entities.objects.get(pk=data['eid']).delete()
        response.status_code = 203
    except Exception:
        response.status_code = 500
    return response

def can_request(request):
    uid = ''
    data = QueryDict.dict(request.POST)
    # response = jwt_precheck(request)
    # if response.status_code in [401, 405]:
    #     uid = 'u1'  # Anonymous
    #     response.status_code = 200
    # else:
    uid = try_get_user(request)
    response = HttpResponse()
    response.content = can(data["uid"] if "uid" in data else uid, data["eid"], data["codename"])
    return response


def can(uid, eid, codename):
    try:
        if uid == 'u0':  # Root
            return True
        e = Entities.objects.get(pk=eid)
        if e.owner.uid == uid:  # Owner
            return True
        if e.is_private:  # Entity is private
            return False
        user = Usr.objects.get(uid=uid)
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
