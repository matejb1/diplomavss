# Custom functions
import jwt
import re
from django.db import connection
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from ALGator.settings import SECRET_KEY


def get_tokens_from_cookie(request: HttpResponse) -> dict:
    if request is None or not (hasattr(request, 'META') and "HTTP_COOKIE" in request.META):
        return {}

    try:
        cookies = request.META["HTTP_COOKIE"].split("; ")
        tokens = {}
        for item in cookies:
            if "refresh" in item:
                tokens["refresh"] = item.split("=")[1]
            elif "access" in item:
                tokens["access"] = item.split("=")[1]
        return tokens
    except Exception:
        return {}


def get_tokens_from_cookie_response(response: HttpResponse) -> dict:
    if response is None:
        return {}
    try:
        cookies = response.cookies
        tokens = {}
        for item in cookies:
            c = str(cookies[item])
            if "refresh" in item:
                tokens["refresh"] = c.split("=")[1].split(";")[0]
            elif "access" in item:
                tokens["access"] = c.split("=")[1].split(";")[0]
        return tokens
    except Exception:
        return {}


def get_credentials_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {"uid": payload["uid"],
                "username": payload["username"],
                "is_superuser": payload["is_superuser"]}
    except Exception:
        return {}


def try_to_get_tokens(request: HttpResponse) -> dict:
    if request is None:
        return {}
    tokens = {}
    try:
        if hasattr(request, 'META') and "HTTP_AUTHORIZATION" in request.META:
            tokens = {"access": request.META['HTTP_AUTHORIZATION'].split(" ")[1]}
        elif hasattr(request, 'META'):
            tokens = get_tokens_from_cookie(request)
        else:
            tokens = get_tokens_from_cookie_response(request)
        return tokens
    except Exception:
        return {}


def try_get_user(response: HttpResponse) -> str:
    try:
        return get_credentials_jwt(try_to_get_tokens(response)["access"])["uid"]
    except Exception:
        return 'u1'


def check_jwt(request: HttpResponse) -> HttpResponse:
    if request is None:
        return None
    response = HttpResponse()
    # tokens = get_tokens_from_cookie(request)
    try:
        tokens = try_to_get_tokens(request)
        if "refresh" in tokens:
            payload_refresh = jwt.decode(tokens["refresh"], SECRET_KEY, algorithms=['HS256'])
            response.set_cookie("refresh", tokens["refresh"])

        if "access" in tokens:
            payload_access = jwt.decode(tokens["access"], SECRET_KEY, algorithms=['HS256'])
            response.set_cookie("access", tokens["access"])
    except jwt.ExpiredSignatureError:
        new_access_token = str(RefreshToken(tokens["refresh"]).access_token)
        response.set_cookie("access", new_access_token)
    except Exception:
        response = None
    return response


def jwt_precheck(request: HttpResponse) -> HttpResponse:
    response = HttpResponse()
    try:
        response = check_jwt(request)
    except Exception:
        response = None
    if response is None:
        response = HttpResponse({"Error": "Unauthorized"})
        response.status_code = 401
    return response


def run_query(query: str, query_parameters=[]) -> list:
    try:
        data = None
        if connection is None or connection.cursor() is None or is_null_or_empty(query):
            return []
        with connection.cursor() as cursor:
            cursor.execute(query, query_parameters)
            data = list(cursor.fetchall())
        return data
    except Exception:
        return []


def validate_request_and_execute(method: str, request: HttpResponse, function_service, id=None) -> HttpResponse:
    if request is None:
        return HttpResponse({"Error": "Bad request"}, status=400)
    try:
        if request.method == method:
            response = jwt_precheck(request)

            if response is None:
                response = HttpResponse({"Error": "Internal server error"}, status=500)

            if response.status_code in [401, 405, 500]:
                return response

            if request.method == 'GET':
                response = function_service(response, id)
            else:
                data = QueryDict.dict(request.POST)
                response = function_service(response, data)
        else:
            response = HttpResponse({"Error": "Method not allowed."}, status=405)
    except Exception:
        response = HttpResponse({"Error": "Internal server error"}, status=500)
    return response


def contains(id, p):
    return (id & p) == p


def is_null_or_empty(item: str) -> bool:
    """Check if item is None or empty.

    Args:
        item (str): Parameter for checking

    Returns:
        bool: Return True if item is not empty or None.
    """
    return item is None or not item.strip()


def is_valid_id(prefix: str, data: str) -> bool:
    """This function check if data is valid id, with following prefix.

    Args:
        prefix (str): allows only {u, g, e, et, p, pt}
        data (str): id

    Returns:
        bool: Checks if data is valid.
    """
    return prefix in ['u', 'g', 'e', 'et', 'p', 'pt'] and not is_null_or_empty(data) and re.match(r"^"+prefix+r"[0-9]+$", data)
