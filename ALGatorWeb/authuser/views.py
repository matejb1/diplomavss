import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from . import service
from .helper import *
from .models import User, Group
from .serializers import serialize_datetime, MyTokenObtainPairSerializer


# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# REST endpoints
@api_view(['POST'])
def add_user_permission(request):
    return validate_request_and_execute('POST', request, service.add_permission_to_user)

@api_view(['POST'])
def add_group_permission(request):
    return validate_request_and_execute('POST', request, service.add_permission_to_group)

@api_view(['POST'])
def add_group(request):
    return validate_request_and_execute('POST', request, service.add_user_to_group)


@api_view(['DELETE'])
def remove_group(request):
    return validate_request_and_execute('DELETE', request, service.remove_user_from_group)


@api_view(['DELETE'])
def remove_user_permission(request):
    return validate_request_and_execute('DELETE', request, service.remove_user_permission)

@api_view(['DELETE'])
def remove_group_permission(request):
    return validate_request_and_execute('DELETE', request, service.remove_group_permission)



# Render page-s
def manage_users_view(request):
    precheck = is_valid_user(request)
    if precheck is not None:
        return precheck

    users = User.objects.all().values()
    return render(request,
                  'cpindex.html', {
                      'contentpage': 'manage_users.html',
                      'users': json.dumps(list(users),
                                          default=serialize_datetime),
                  }
                  )


def manage_single_user_view(request, id):
    precheck = is_valid_user(request)
    if precheck is not None:
        return precheck

    user = None
    try:
        # All OK. Superuser has full access.
        data = service.get_single_user_data_view(id)
        return render(request,
                      'cpindex.html',
                      {'contentpage': 'manage_single_user.html',
                       'data': data}
                      )
    except Exception:
        # User doesn't exists.
        return render(request,
                      'cpindex.html',
                      {
                          'contentpage': 'users_groups_error_page.html',
                          'msg': f'Following user with user id {id}, cannot be found.'
                      },
                      status=500
                      )


def manage_groups_view(request):
    precheck = is_valid_user(request)
    if precheck is not None:
        return precheck

    groups = Group.objects.all()
    return render(request,
                  'cpindex.html',
                  {'contentpage': 'manage_groups.html',
                   'groups': json.dumps([{"id": g.id,
                                          "name": g.name} for g in groups]),
                   }
                  )


def manage_single_group_view(request, id):
    precheck = is_valid_user(request)
    if precheck is not None:
        return precheck
    try:
        # All OK. Superuser has full access.
        data = service.get_single_group_data_view(id)

        return render(request,
                      'cpindex.html',
                      {'contentpage': 'manage_single_group.html',
                              'data': data}
                      )
    except Exception:
        # Group doesn't exists.
        return render(request,
                      'cpindex.html',
                      {'contentpage': 'users_groups_error_page.html',
                              'msg': f'Following group with group id {id}, cannot be found.'
                                },
                      status=500
                      )

