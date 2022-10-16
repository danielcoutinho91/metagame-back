from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .utils import Utils, UserUtils, MediaTypeUtils, GoalUtils

@api_view(['GET'])
def routes(request):
    return Utils.get_routes()

# USER ------------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def unauthorized(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def me(request):
    return UserUtils.get_me(request)

@api_view(['GET', 'POST'])
def user(request):
    if request.method == "GET":
        return UserUtils.get_all_users()

    elif request.method == "POST":
        return UserUtils.create_user(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET', 'PUT', 'DELETE'])
def user_by_id(request, user_id):
    if request.method == 'GET':
        return UserUtils.get_user_by_id(request, user_id)

    elif request.method == 'PUT':
        return UserUtils.update_user(request, user_id)

    elif request.method == 'DELETE':
        return UserUtils.delete_user(request, user_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def user_by_username_or_email(request, username):
    if request.method == 'GET':
        return UserUtils.get_user_by_username_or_email(request, username)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        return UserUtils.login(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def logout(request):
    return UserUtils.logout(request)

# MEDIA TYPE ------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def media_type(request):
    return MediaTypeUtils.get_all_media_type()

# GOAL ------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/api/unauthorized')
@api_view(['GET', 'POST'])
def goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(0, 0)

    elif request.method == "POST":
        return GoalUtils.create_goal(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def active_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(0, 1)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def inactive_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(0, 2)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def done_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(0, 3)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def movie_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(1, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def game_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def book_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def movie_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(1, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(1, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(3, 3)
        else:
            return GoalUtils.get_all_goals(1, 0)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def game_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(2, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(2, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(2, 3)
        else:
            return GoalUtils.get_all_goals(2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def book_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(3, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(3, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(3, 3)
        else:
            return GoalUtils.get_all_goals(3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET', 'DELETE'])
def goal_by_id(request, goal_id):
    if request.method == 'GET':
        return GoalUtils.get_goal_by_id(request, goal_id)

    elif request.method == 'DELETE':
        return GoalUtils.delete_goal(request, goal_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 0, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def movie_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 1, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def game_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 2, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def book_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 3, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def goals_by_user_and_activity(request, user_id, is_active):
    if request.method == 'GET':
        if is_active == 'active':
            return GoalUtils.get_all_goals_by_user(request, 0, 1, user_id)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals_by_user(request, 0, 2, user_id)
        elif is_active == 'done':
            return GoalUtils.get_all_goals_by_user(request, 0, 3, user_id)
        else:
            return GoalUtils.get_all_goals_by_user(request, 0, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def movie_goals_by_user_and_activity(request, user_id, is_active):
    if request.method == 'GET':
        if is_active == 'active':
            return GoalUtils.get_all_goals_by_user(request, 1, 1, user_id)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals_by_user(request, 1, 2, user_id)
        elif is_active == 'done':
            return GoalUtils.get_all_goals_by_user(request, 1, 3, user_id)
        else:
            return GoalUtils.get_all_goals_by_user(request, 1, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def game_goals_by_user_and_activity(request, user_id, is_active):
    if request.method == 'GET':
        if is_active == 'active':
            return GoalUtils.get_all_goals_by_user(request, 2, 1, user_id)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals_by_user(request, 2, 2, user_id)
        elif is_active == 'done':
            return GoalUtils.get_all_goals_by_user(request, 2, 3, user_id)
        else:
            return GoalUtils.get_all_goals_by_user(request, 2, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/unauthorized')
@api_view(['GET'])
def book_goals_by_user_and_activity(request, user_id, is_active):
    if request.method == 'GET':
        if is_active == 'active':
            return GoalUtils.get_all_goals_by_user(request, 3, 1, user_id)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals_by_user(request, 3, 2, user_id)
        elif is_active == 'done':
            return GoalUtils.get_all_goals_by_user(request, 3, 3, user_id)
        else:
            return GoalUtils.get_all_goals_by_user(request, 3, 0, user_id)
        
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)