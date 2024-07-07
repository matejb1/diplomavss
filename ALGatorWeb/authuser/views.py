import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from . import service
from .helper import *
from .serializers import serialize_datetime, MyTokenObtainPairSerializer


# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# REST endpoints
@api_view(['GET'])
def get_users(request):
    return validate_request_and_execute('GET', request, service.get_users)

@api_view(['GET'])
def get_all_permission_types(request):
    return service.get_all_permission_types(request)

@api_view(['GET'])
def get_user(request, id):
    return validate_request_and_execute('GET', request, service.get_user, id)

@api_view(['POST'])
def get_groups(request):
    return validate_request_and_execute('POST', request, service.get_groups)

@api_view(['GET'])
def get_groups_user(request):
    # return validate_request_and_execute('GET', request, service.get_groups_user)
    return service.get_groups_user(request)


@api_view(['POST'])
def get_all_user_permissions_by_eid(request):
    return validate_request_and_execute('POST', request, service.get_all_user_permissions_by_eid)

@api_view(['GET'])
def entities_permissions(request):
    # return validate_request_and_execute('GET', request, service.entities_permissions)
    return service.entities_permissions(request)

@api_view(['GET'])
def get_entities(request):
    #return validate_request_and_execute('GET', request, service.get_entities)
    return service.get_entities(request)


@api_view(['PUT'])
def edit_user(request):
    return validate_request_and_execute('PUT', request, service.edit_user)




@api_view(['POST'])
def can(request):
    return service.can_request(request)


@api_view(['PUT'])
def add_user_permission(request):
    return validate_request_and_execute('PUT', request, service.add_permission_to_user)

@api_view(['PUT'])
def add_group_permission(request):
    return validate_request_and_execute('PUT', request, service.add_permission_to_group)

@api_view(['POST'])
def add_group(request):
    return validate_request_and_execute('POST', request, service.add_group)

@api_view(['DELETE'])
def remove_user_from_group(request):
    return validate_request_and_execute('DELETE', request, service.remove_user_from_group)

@api_view(['DELETE'])
def remove_user(request):
    return validate_request_and_execute('DELETE', request, service.remove_user)


@api_view(['DELETE'])
def remove_group(request):
    return validate_request_and_execute('DELETE', request, service.remove_group)

@api_view(['POST'])
def add_user(request):
    return validate_request_and_execute('POST', request, service.add_user)


@api_view(['POST'])
def add_user_to_group(request):
    return validate_request_and_execute('POST', request, service.add_user_to_group)

@api_view(['POST'])
def add_entity(request):
    return validate_request_and_execute('POST', request, service.add_entity)

@api_view(['DELETE'])
def remove_entity(request):
    return validate_request_and_execute('DELETE', request, service.remove_entity)



@api_view(['PUT'])
def update_user_permission(request):
    return validate_request_and_execute('PUT', request, service.update_user_permission)

@api_view(['PUT'])
def update_group_permission(request):
    return validate_request_and_execute('PUT', request, service.update_group_permission)



# Render page-s
def manage_users_view(request):
    # precheck = is_valid_user(request)
    # if precheck is not None:
    #     return precheck

    uid = request.user.uid if request.user.is_authenticated else 'u1'
    if service.can(uid, 'e0', 'can_edit_users'):
        return render(request,
                  'cpindex.html',
                       {'contentpage': 'manage_users.html'}
                    )
    else:
        return render(request, 'cpindex.html',
                      {'contentpage': 'users_groups_error_page.html',
                              'msg': 'Permission denied!'})



def manage_single_user_view(request, id):
    # precheck = is_valid_user(request)
    # if precheck is not None:
    #     return precheck
    uid = request.user.uid if request.user.is_authenticated else 'u1'
    if service.can(uid, 'e0', 'can_edit_users'):
        return render(request,
                  'cpindex.html',
                       {'contentpage': 'manage_single_user.html',
                               'user_id': id}
                    )
    else:
        return render(request, 'cpindex.html',
                      {'contentpage': 'users_groups_error_page.html',
                              'msg': 'Permission denied!'})


def manage_rights_view(request):
    # precheck = is_valid_user(request)
    # if precheck is not None:
    #     return precheck
    uid = request.user.uid if request.user.is_authenticated else 'u1'
    if service.can(uid, 'e0', 'can_edit_rights'):
        return render(request,
                  'cpindex.html',
                       {'contentpage': 'manage_rights.html'}
                    )
    else:
        return render(request, 'cpindex.html',
                      {'contentpage': 'users_groups_error_page.html',
                              'msg': 'Permission denied!'})
