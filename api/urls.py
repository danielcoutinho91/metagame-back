from django.urls import path
from . import views

urlpatterns = [
    path('', views.routes, name='routes'),
    path('unauthorized', views.unauthorized, name='unauthorized'),
    path('user', views.user, name='users'),
    path('user/<str:pk>', views.user_by_id, name='user'),
    path('user/find/<str:pk>', views.user_by_username_or_email, name='user_by_username_or_email'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]