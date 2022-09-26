from django.urls import path
from . import views

urlpatterns = [
    path('', views.routes, name='routes'),
    path('user', views.user, name='users'),
    path('user/<str:pk>', views.user_by_id, name='users'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]