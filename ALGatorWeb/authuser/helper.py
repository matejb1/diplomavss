# Custom functions
import jwt
from django.db import connection
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from ALGator.settings import SECRET_KEY


def get_tokens_from_cookie(request):
    cookies = request.META["HTTP_COOKIE"].split("; ")
    tokens = {}
    for item in cookies:
        if "refresh" in item:
            tokens["refresh"] = item.split("=")[1]
        elif "access" in item:
            tokens["access"] = item.split("=")[1]
    return tokens


def get_credentials_jwt(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return {"user_id": payload["user_id"],
            "username": payload["username"],
            "is_superuser": payload["is_superuser"]}


def check_jwt(request):
    response = HttpResponse()
    tokens = get_tokens_from_cookie(request)
    try:
        payload_refresh = jwt.decode(tokens["refresh"], SECRET_KEY, algorithms=['HS256'])
        response.set_cookie("refresh", tokens["refresh"])

        payload_access = jwt.decode(tokens["access"], SECRET_KEY, algorithms=['HS256'])
        response.set_cookie("access", tokens["access"])
    except jwt.ExpiredSignatureError:
        new_access_token = str(RefreshToken(tokens["refresh"]).access_token)
        response.set_cookie("access", new_access_token)
    except Exception:
        response = None
    return response


def jwt_precheck(request):
    response = check_jwt(request)
    if response is None:
        response = HttpResponse({"Error": "Unauthorized"})
        response.status_code = 401
    return response


def run_query(query, query_parameters=[]):
    data = None
    with connection.cursor() as cursor:
        cursor.execute(query, query_parameters)
        data = list(cursor.fetchall())
    return data

def validate_request_and_execute(method, request, function_service):
    if request.method == method:
        response = jwt_precheck(request)
        if response.status_code in [401, 405]:
            return response
        credentials = get_credentials_jwt(response.cookies["access"].value)
        if credentials["is_superuser"] == 1:
            data = QueryDict.dict(request.POST)
            response = function_service(response, data)
        else:
            response = HttpResponse({"Error": "You're not a superuser."}, status=401)
    else:
        response = HttpResponse({"Error": "Method not allowed."}, status=405)
    return response

def is_valid_user(request):
    if not request.user.is_authenticated:
        return render(request,
                      'cpindex.html',
                      {
                          'contentpage': 'users_groups_error_page.html',
                          'msg': 'First you need to be logged, if you want\'t access this view.'
                      },
                      status=500
                      )
    elif request.user.is_authenticated and not request.user.is_superuser:
        return render(request,
                      'cpindex.html',
                      {
                          'contentpage': 'users_groups_error_page.html',
                          'msg': f'Following user: {request.user.username} hasn\'t permission to access this view.'
                      },
                      status=500
                      )
    return None


# TODO: add_entity --> te zadejve implemetiri v JAVI
def add_entity(user, entity_id, is_private, entity_type):
    pass


# TODO: probably remove enttity

# TODO: can: T/F --> te zadejve implemetiri v JAVI + Javascript
def can(user, entity_id, permission):
    pass
