from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from .utils import Utils, UserUtils

@api_view(['GET'])
def routes(request):
    return Utils.get_routes()

# USER ------------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def guest(request):
    HttpResponse("Necessário fazer login")


@api_view(['GET', 'POST'])
def user(request):
    if request.method == "GET":
        return UserUtils.get_all_users()

    elif request.method == "POST":
        return UserUtils.create_user(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# @login_required(login_url='/api/login')
@api_view(['GET', 'PUT', 'DELETE'])
def user_by_id(request, pk):
    current_user = request.user
    print(f"CURRENT USER: {current_user}")

    if request.method == 'GET':
        return UserUtils.get_user_by_id(request, pk)

    elif request.method == 'PUT':
        return UserUtils.update_user(request, pk)

    elif request.method == 'DELETE':
        return UserUtils.delete_user(request, pk)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def user_by_username_or_email(request, pk):

    if request.method == 'GET':
        return UserUtils.get_user_by_username_or_email(request, pk)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        return UserUtils.login(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def logout(request):
    return UserUtils.logout(request)