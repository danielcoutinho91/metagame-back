from django.urls import path
from . import views

urlpatterns = [
    path('', views.routes, name='routes'),
    path('unauthorized', views.unauthorized, name='unauthorized'),

    path('me', views.me, name='me'),
    path('users', views.user, name='user'),
    path('users/<str:user_id>', views.user_by_id, name='user_by_id'),
    path('users/find/<str:username>', views.user_by_username_or_email, name='user_by_username_or_email'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('mediatypes', views.media_type, name='media_type'),

    path('goals', views.goal, name='goal'),
    path('goals/active', views.active_goal, name='active_goal'),
    path('goals/inactive', views.inactive_goal, name='inactive_goal'),
    path('goals/done', views.done_goal, name='done_goal'),
    path('goals/movies', views.movie_goals, name='movie_goals'),
    path('goals/games', views.game_goals, name='game_goals'),
    path('goals/books', views.book_goals, name='book_goals'),
    path('goals/movies/<str:is_active>', views.movie_goals_by_activity, name='movie_goals_by_activity'),
    path('goals/games/<str:is_active>', views.game_goals_by_activity, name='game_goals_by_activity'),
    path('goals/books/<str:is_active>', views.book_goals_by_activity, name='book_goals_by_activity'),
    path('goals/<str:goal_id>', views.goal_by_id, name='goal_by_id'),
    path('goals/user/<str:user_id>', views.goals_by_user, name='goals_by_user'),
    path('goals/user/<str:user_id>/movies', views.movie_goals_by_user, name='movie_goals_by_user'),
    path('goals/user/<str:user_id>/games', views.game_goals_by_user, name='game_goals_by_user'),
    path('goals/user/<str:user_id>/books', views.book_goals_by_user, name='book_goals_by_user'),
    path('goals/user/<str:user_id>/<str:is_active>', views.goals_by_user_and_activity, name='goals_by_user_and_activity'),
    path('goals/user/<str:user_id>/movies/<str:is_active>', views.movie_goals_by_user_and_activity, name='movie_goals_by_user_and_activity'),
    path('goals/user/<str:user_id>/games/<str:is_active>', views.game_goals_by_user_and_activity, name='game_goals_by_user_and_activity'),
    path('goals/user/<str:user_id>/books/<str:is_active>', views.book_goals_by_user_and_activity, name='book_goals_by_user_and_activity'),
]