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
    path('meta/ativa', views.meta_ativa, name='meta_ativa'),
    path('meta/inativa', views.meta_inativa, name='meta_inativa'),
    path('meta/cumprida', views.meta_cumprida, name='meta_cumprida'),
    path('meta/filme', views.metas_filmes, name='metas_filmes'),
    path('meta/jogo', views.metas_jogos, name='metas_jogos'),
    path('meta/livro', views.metas_livros, name='metas_livros'),
    path('meta/filme/<str:is_ativa>', views.metas_filmes_by_atividade, name='metas_filmes_by_atividade'),
    path('meta/jogo/<str:is_ativa>', views.metas_jogos_by_atividade, name='metas_jogos_by_atividade'),
    path('meta/livro/<str:is_ativa>', views.metas_livros_by_atividade, name='metas_livros_by_atividade'),
    path('meta/<str:pk>', views.meta_by_id, name='meta_by_id'),
    path('meta/user/<str:pk>', views.metas_by_user, name='metas_by_user'),
    path('meta/filme/user/<str:pk>', views.metas_filmes_by_user, name='metas_filmes_by_user'),
    path('meta/jogo/user/<str:pk>', views.metas_jogos_by_user, name='metas_jogos_by_user'),
    path('meta/livro/user/<str:pk>', views.metas_livros_by_user, name='metas_livros_by_user'),
    path('meta/user/<str:pk>/<str:is_ativa>', views.metas_by_user_and_atividade, name='metas_by_user_and_atividade'),
    path('meta/filme/user/<str:pk>/<str:is_ativa>', views.metas_filmes_by_user_and_atividade, name='metas_filmes_by_user_and_atividade'),
    path('meta/jogo/user/<str:pk>/<str:is_ativa>', views.metas_jogos_by_user_and_atividade, name='metas_jogos_by_user_and_atividade'),
    path('meta/livro/user/<str:pk>/<str:is_ativa>', views.metas_livros_by_user_and_atividade, name='metas_livros_by_user_and_atividade'),
]