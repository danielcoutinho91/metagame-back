from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .utils import Utils, UserUtils, TipoMidiaUtils, MetaUtils

@api_view(['GET'])
def routes(request):
    return Utils.get_routes()

# USER ------------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def guest(request):
    HttpResponse("Necessário fazer login")

@api_view(['GET'])
def unauthorized(request):
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def user(request):
    if request.method == "GET":
        return UserUtils.get_all_users()

    elif request.method == "POST":
        return UserUtils.create_user(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET', 'PUT', 'DELETE'])
def user_by_id(request, pk):
    if request.method == 'GET':
        return UserUtils.get_user_by_id(request, pk)

    elif request.method == 'PUT':
        return UserUtils.update_user(request, pk)

    elif request.method == 'DELETE':
        return UserUtils.delete_user(request, pk)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
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

# TIPOMIDIA -------------------------------------------------------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def tipo_midia(request):
    return TipoMidiaUtils.get_all_tipo_midia()

# META ------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/api/guest')
@api_view(['GET', 'POST'])
def meta(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(0, 0)

    elif request.method == "POST":
        return MetaUtils.create_meta(request)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def meta_ativa(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(0, 1)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def meta_inativa(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(0, 2)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def meta_cumprida(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(0, 3)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_filmes(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(1, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_jogos(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_livros(request):
    if request.method == "GET":
        return MetaUtils.get_all_metas(3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_filmes_by_atividade(request, is_ativa):
    if request.method == "GET":
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas(1, 1)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas(1, 2)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas(3, 3)
        else:
            return MetaUtils.get_all_metas(1, 0)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_jogos_by_atividade(request, is_ativa):
    if request.method == "GET":
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas(2, 1)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas(2, 2)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas(2, 3)
        else:
            return MetaUtils.get_all_metas(2, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_livros_by_atividade(request, is_ativa):
    if request.method == "GET":
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas(3, 1)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas(3, 2)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas(3, 3)
        else:
            return MetaUtils.get_all_metas(3, 0)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET', 'DELETE'])
def meta_by_id(request, pk):
    if request.method == 'GET':
        return MetaUtils.get_meta_by_id(request, pk)

    elif request.method == 'DELETE':
        return MetaUtils.delete_meta(request, pk)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_by_user(request, pk):
    if request.method == 'GET':
        return MetaUtils.get_all_metas_by_user(request, 0, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_filmes_by_user(request, pk):
    if request.method == 'GET':
        return MetaUtils.get_all_metas_by_user(request, 1, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_jogos_by_user(request, pk):
    if request.method == 'GET':
        return MetaUtils.get_all_metas_by_user(request, 2, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_livros_by_user(request, pk):
    if request.method == 'GET':
        return MetaUtils.get_all_metas_by_user(request, 3, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_by_user_and_atividade(request, pk, is_ativa):
    if request.method == 'GET':
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas_by_user(request, 0, 1, pk)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas_by_user(request, 0, 2, pk)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas_by_user(request, 0, 3, pk)
        else:
            return MetaUtils.get_all_metas_by_user(request, 0, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_filmes_by_user_and_atividade(request, pk, is_ativa):
    if request.method == 'GET':
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas_by_user(request, 1, 1, pk)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas_by_user(request, 1, 2, pk)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas_by_user(request, 1, 3, pk)
        else:
            return MetaUtils.get_all_metas_by_user(request, 1, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_jogos_by_user_and_atividade(request, pk, is_ativa):
    if request.method == 'GET':
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas_by_user(request, 2, 1, pk)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas_by_user(request, 2, 2, pk)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas_by_user(request, 2, 3, pk)
        else:
            return MetaUtils.get_all_metas_by_user(request, 2, 0, pk)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/api/guest')
@api_view(['GET'])
def metas_livros_by_user_and_atividade(request, pk, is_ativa):
    if request.method == 'GET':
        if is_ativa == 'ativa':
            return MetaUtils.get_all_metas_by_user(request, 3, 1, pk)
        elif is_ativa == 'inativa':
            return MetaUtils.get_all_metas_by_user(request, 3, 2, pk)
        elif is_ativa == 'cumprida':
            return MetaUtils.get_all_metas_by_user(request, 3, 3, pk)
        else:
            return MetaUtils.get_all_metas_by_user(request, 3, 0, pk)
        
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)