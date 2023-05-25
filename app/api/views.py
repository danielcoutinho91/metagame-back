from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from django.contrib.auth.decorators import login_required
from .utils import Utils, UserUtils, MediaTypeUtils, GoalUtils, FavoriteGoalsUtils, MediaUtils, RankingUtils

@api_view(['GET'])
def routes(request):
    return Utils.get_routes()

# USER ------------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def unauthorized(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes((IsAuthenticated, ))
def user_by_id(request, user_id):
    if request.method == 'GET':
        return UserUtils.get_user_by_id(request, user_id)

    elif request.method == 'PUT':
        return UserUtils.update_user(request, user_id)

    elif request.method == 'DELETE':
        return UserUtils.delete_user(request, user_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 0, 0)

    elif request.method == "POST":
        return GoalUtils.create_goal(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def active_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 0, 1)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def inactive_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 0, 2)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def done_goal(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 0, 3)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def movie_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 1, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def game_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def book_goals(request):
    if request.method == "GET":
        return GoalUtils.get_all_goals(request, 3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def movie_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(request, 1, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(request, 1, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(request, 1, 3)
        else:
            return GoalUtils.get_all_goals(request, 1, 0)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def game_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(request, 2, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(request, 2, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(request, 2, 3)
        else:
            return GoalUtils.get_all_goals(request, 2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def book_goals_by_activity(request, is_active):
    if request.method == "GET":
        if is_active == 'active':
            return GoalUtils.get_all_goals(request, 3, 1)
        elif is_active == 'inactive':
            return GoalUtils.get_all_goals(request, 3, 2)
        elif is_active == 'done':
            return GoalUtils.get_all_goals(request, 3, 3)
        else:
            return GoalUtils.get_all_goals(request, 3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE'])
# @permission_classes((IsAuthenticated, ))
def goal_by_id(request, goal_id):
    if request.method == 'GET':
        return GoalUtils.get_goal_by_id(request, goal_id)

    elif request.method == 'DELETE':
        return GoalUtils.delete_goal(request, goal_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 0, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def movie_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 1, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def game_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 2, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def book_goals_by_user(request, user_id):
    if request.method == 'GET':
        return GoalUtils.get_all_goals_by_user(request, 3, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
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

# GOAL LIKES ------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def favorite_goals(request):
    if request.method == 'GET':
        return FavoriteGoalsUtils.get_all_favorite_goals(request)
    
    elif request.method == "POST":
        return FavoriteGoalsUtils.create_or_delete_favorite_goal(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def favorite_goals_by_user(request, user_id):
    if request.method == 'GET':
        return FavoriteGoalsUtils.get_all_favorite_goals_by_user(request, user_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# MEDIA -----------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def media(request):
    if request.method == "GET":
        return MediaUtils.get_all_medias(0)

    elif request.method == "POST":
        return MediaUtils.create_media(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def movie_medias(request):
    if request.method == "GET":
        return MediaUtils.get_all_medias(1)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def game_medias(request):
    if request.method == "GET":
        return MediaUtils.get_all_medias(2)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def book_medias(request):
    if request.method == "GET":
        return MediaUtils.get_all_medias(3)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE'])
# @permission_classes((IsAuthenticated, ))
def media_by_id(request, media_id):
    if request.method == 'GET':
        return MediaUtils.get_media_by_id(request, media_id)

    # elif request.method == 'DELETE':
    #     return MediaUtils.delete_media(request, media_id)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def medias_by_user(request, user_id):
    if request.method == 'GET':
        return MediaUtils.get_all_medias_by_user(request, 0, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def movie_medias_by_user(request, user_id):
    if request.method == 'GET':
        return MediaUtils.get_all_medias_by_user(request, 1, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def game_medias_by_user(request, user_id):
    if request.method == 'GET':
        return MediaUtils.get_all_medias_by_user(request, 2, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def book_medias_by_user(request, user_id):
    if request.method == 'GET':
        return MediaUtils.get_all_medias_by_user(request, 3, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def medias_by_goal(request, goal_id):
    if request.method == 'GET':
        return MediaUtils.get_all_medias_by_goal(request, goal_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def medias_top(request):
    if request.method == 'GET':
        return RankingUtils.get_medias_top(request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def medias_top_by_type(request, mediatype):
    if request.method == 'GET':
        if mediatype == 'movies':
            return RankingUtils.get_medias_top_by_type(request, 1)
        if mediatype == 'games':
            return RankingUtils.get_medias_top_by_type(request, 2)
        if mediatype == 'books':
            return RankingUtils.get_medias_top_by_type(request, 3)
        return RankingUtils.get_medias_top(request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# RANKING ---------------------------------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def ranking(request):
    if request.method == 'GET':
        return RankingUtils.get_ranking(request, -1)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def ranking_by_type(request, mediatype):
    if request.method == 'GET':
        if mediatype == 'movies':
            return RankingUtils.get_ranking_by_type(request, -1, 1)
        if mediatype == 'games':
            return RankingUtils.get_ranking_by_type(request, -1, 2)
        if mediatype == 'books':
            return RankingUtils.get_ranking_by_type(request, -1, 3)
        return RankingUtils.get_ranking(request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def ranking_by_user(request, user_id):
    if request.method == 'GET':
        return RankingUtils.get_ranking(request, user_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def ranking_by_user_and_type(request, user_id, mediatype):
    if request.method == 'GET':
        if mediatype == 'movies':
            return RankingUtils.get_ranking_by_type(request, user_id, 1)
        if mediatype == 'games':
            return RankingUtils.get_ranking_by_type(request, user_id, 2)
        if mediatype == 'books':
            return RankingUtils.get_ranking_by_type(request, user_id, 3)
        return RankingUtils.get_ranking(request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
        