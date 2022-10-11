from django.urls import path
from . import views

urlpatterns = [
    path('', views.routes, name='routes'),
    path('unauthorized', views.unauthorized, name='unauthorized'),

    path('user', views.user, name='user'),
    path('user/<str:pk>', views.user_by_id, name='user_by_id'),
    path('user/find/<str:pk>', views.user_by_username_or_email, name='user_by_username_or_email'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('tipomidia', views.tipo_midia, name='tipo_midia'),

    path('meta', views.meta, name='meta'),
    # path('meta/<str:pk>', views.meta_by_id, name='meta_by_id'),
    # path('meta/find/<str:pk>', views.meta_by_user, name='meta_by_user'),
]