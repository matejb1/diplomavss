import json

from django.contrib.auth.models import User
from django.core import serializers
from django.http import QueryDict, HttpResponse

from .helper import run_query, jwt_precheck, contains, try_get_user
from .models import Group, PermissionType, EntityPermissionUser, Entities, EntityPermissionGroup, Group_User, User as Usr
from .queries import *


def add_group(response, data):
    try:
        uid = Usr.objects.get(pk=try_get_user(response))
        gid = f"g{int(Group.objects.latest('id').id[1:])+1}"
        Group.objects.get_or_create(id=gid, name=data['name'], owner=uid)
        response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    return response


def add_user_to_group(response, data):
    response.content_type = "application/json"
    try:
        uid = Usr.objects.get(user=User.objects.get(username=data["username"]))
        gid = Group.objects.get(pk=data["gid"])

        Group_User.objects.get_or_create(user=uid, group=gid)
        response.status_code = 201
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}

    return response


def edit_user(response, data):
    try:
        uid = User.objects.get(pk=data['id'])
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
        uid = Usr.objects.get(pk=u)
        Group.objects.get(pk=data['group_id']).delete()
        response.status_code = 203
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response

def remove_user_from_group(response, data):
    response.content_type = "application/json"
    try:
        uid = Usr.objects.get(user=User.objects.get(username=data["username"]))
        gid = Group.objects.get(pk=data["gid"])
        Group_User.objects.get(user=uid, group=gid).delete()
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User isn't present in this group."}
    return response

def add_permission_to_user(response, data):
    try:
        pid = PermissionType.objects.get(pk=data["permission_id"])
        eid = Entities.objects.get(pk=data["entity_id"])

        usr = try_get_user(response)
        if not can(usr, eid, 'p1'):
            raise Exception
        uid = Usr.objects.get(user=User.objects.get(username=data["id"]))

        epu, created = EntityPermissionUser.objects.get_or_create(entity=eid, user=uid)
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
    pid = PermissionType.objects.get(pk=data["permission_id"])
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
    uid = Usr.objects.get(pk=data["id"])
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
        uid = Usr.objects.get(pk=try_get_user(request))
        response = HttpResponse()
        data = []
        if uid.pk == 'u0':
            data = Entities.objects.all()
        else:
            data.extend(Entities.objects.filter(owner=uid))
            for gu in Group_User.objects.filter(user=uid):
                for epg in EntityPermissionGroup.objects.filter(group=gu.group):
                    if epg.entity not in data:
                        data.append(epg.entity)

            for epu in EntityPermissionUser.objects.filter(user=uid):
                if epu.entity not in data:
                    data.append(epu.entity)
    except Exception:
        response.status_code = 500
        response.content = {"Error": "User exists in this group."}
    response.content = serializers.serialize("json", data, )
    response.content_type = "application/json"
    return response

def get_users(response, *args):
    users = serializers.serialize("json", User.objects.all(),
                                  fields=["username", "email", "is_superuser"])
    response.content = users
    response.content_type = "application/json"
    return response


def get_user(response, id):
    user = serializers.serialize('json', [User.objects.get(pk=id), ],
                                 fields=["username", "email", "is_superuser", "is_staff", "is_active"])
    response.content = user
    response.content_type = "application/json"
    return response


def get_groups_user(request, *args):
    try:
        uid = Usr.objects.get(pk=try_get_user(request))
        response = HttpResponse()
        g = []
        if uid.pk == 'u0':  # root
            g = Group.objects.all()
        else:
            g = [gu.group for gu in Group_User.objects.filter(user=uid)]
            g.extend(Group.objects.filter(owner=uid))
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
    uid = Usr.objects.get(pk=try_get_user(response))
    pw = PermissionType.objects.get(codename='can_write').value
    grp = []

    if uid.pk == 'u0':
        grp.extend(Group.objects.all())
    else:
        for gu in Group_User.objects.filter(user=uid):
            try:
                epg = EntityPermissionGroup.objects.get(group=gu.group, entity=eid)
                if contains(epg.value, pw):
                    grp.append(gu.group)
            except Exception:
                continue
        grp.extend(Group.objects.filter(owner=uid))

    groups = serializers.serialize("json", list(set(grp)), )
    response.content = groups
    response.content_type = "application/json"
    return response


def get_all_user_permissions(request, *args):
    response = HttpResponse()
    permissions = serializers.serialize("json", PermissionType.objects.all(), )
    response.content = permissions
    response.content_type = "application/json"
    return response

def entities_permissions(request, *args):
    u = Usr.objects.get(pk=try_get_user(request))
    response = HttpResponse()
    # gids = ", ".join(f'"{g.group.pk}"' for g in Group_User.objects.filter(user=u))
    data = []
    if u.pk == 'u0':
        data = json.dumps(run_query(PERMISSIONS_ENTTIES_USER_GROUP_ROOT, []))
    else:
        data = json.dumps(run_query(PERMISSIONS_ENTTIES_USER_GROUP, [u.pk, u.pk]))
    response.content = data
    response.content_type = "application/json"
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
    response.content = can(data["uid"] if "uid" in data else uid, data["eid"], data["pid"])
    return response


def can(uid, eid, pid):
    try:
        if uid == 'u0':  # Root
            return True
        e = Entities.objects.get(pk=eid)
        if e.owner.pk == uid:  # Owner
            return True
        if e.is_private:  # Entity is private
            return False
        user = Usr.objects.get(pk=uid)
        p = PermissionType.objects.get(pk=pid)
        pfc = PermissionType.objects.get(value=0xFFFF)
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
