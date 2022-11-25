from http.client import HTTPResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.models import User
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from datetime import date, datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, MediaTypeSerializer, GoalSerializer, FavoriteGoalsSerializer, GoalTemplateSerializer, MediaSerializer
from .models import FavoriteGoals, MediaType, Goal, UserInfo, Media

class Utils:
    routes = [
        {
            "user": [
                {
                    'Endpoint': '/api',
                    'method': 'GET',
                    'body': None,
                    'description': 'Retorna um array routes'
                },
                {
                    'Endpoint': '/api/me',
                    'method': 'GET',
                    'body': None,
                    'description': 'Retorna um array com as inforamações do usuário autenticado'
                },
                {
                    'Endpoint': '/api/users',
                    'method': 'GET, POST',
                    'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha", "provider": "", "image_url": ""},
                    'description': 'GET: Retorna um array com todos os usuários do sistema, POST: Cria um novo usuário com os dados da requisição'
                },
                {
                    'Endpoint': '/api/users/:user_id',
                    'method': 'GET, PUT, DELETE',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha", "image_url": ""},
                    'description': 'GET: Retorna o usuário pelo id especificado, PUT: Atualiza o usuário com o id especificado, DELETE: Deleta o usuário com o id especificado'
                },
                {
                    'Endpoint': '/api/users/find/:username_or_email',
                    'method': 'GET, PUT',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {"username": "name"},
                    'description': 'GET: Retorna o usuário pelo id especificado, PUT: Atualiza o usuário com o id especificado'
                },
                {
                    'Endpoint': '/api/login',
                    'method': 'POST',
                    'body': {"username": "name", "password": "senha", "provider": ""},
                    'description': 'Faz login do usuário com dados enviados através de uma requisição POST'
                },
                {
                    'Endpoint': '/api/logout',
                    'method': 'GET',
                    'body': None,
                    'description': 'Faz logout do usuário'
                },
            ],
            "mediatypes": [
                {
                    'Endpoint': '/api/mediatypes',
                    'method': 'GET',
                    'body': None,
                    'description': 'Retorna um array com os tipos de mídia'
                },
            ],
            "goals": [
                {
                    'Endpoint': '/api/goals',
                    'method': 'GET, POST',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {"mediatype": "mediatype_id", "creator": "creator_id", "objective_quantity": "10", "limit_days": "30"},
                    'description': 'GET: Retorna um array com todos as metas do sistema, POST: Cria uma nova meta com os dados da requisição'
                },
                {
                    'Endpoint': '/api/goals/:goal_id',
                    'method': 'GET, DELETE',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna a meta pelo id especificado, DELETE: Deleta a meta com o id especificado'
                },
                {
                    'Endpoint': '/api/goals/:is_active',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas pela status dela. (active / inactive / done)'
                },
                {
                    'Endpoint': '/api/goals/:media_type',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas pelo tipo dela. (movies / games / books)'
                },
                {
                    'Endpoint': '/api/goals/favorites',
                    'method': 'GET, POST',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas favoritas ordenadas por quantidade de likes. POST: Cria ou remove uma meta favorita'
                },
                {
                    'Endpoint': '/api/goals/:media_type/:is_active',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas pelo tipo e status dela. (movies / games / books) / (active / inactive / done)'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas do usuário.'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/:media_type',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas de determinado tipo do usuário. (movies / games / books)'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/favorites',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas favoritas do usuário.'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/:media_type/:is_active',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todas as metas de determinado tipo e status do usuário. (movies / games / books) / (active / inactive / done)'
                },
            ],
            "medias": [
                {
                    'Endpoint': '/api/medias',
                    'method': 'GET, POST',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {"mediatype": "mediatype_id", "id_on_api": "id_on_api", "image_on_api": "image_on_api"},
                    'description': 'GET: Retorna um array com todos os registros de mídias do sistema, POST: Cria um novo registro de mídia com os dados da requisição'
                },
                {
                    'Endpoint': '/api/medias/:media_id',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna o registro de mídias pelo id especificado'
                },
                {
                    'Endpoint': '/api/medias/movies',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de filmes'
                },
                {
                    'Endpoint': '/api/medias/games',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de jogos'
                },
                {
                    'Endpoint': '/api/medias/books',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de livros'
                },
                {
                    'Endpoint': '/api/medias/user/:user_id',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de mídias por usuário'
                },
                {
                    'Endpoint': '/api/medias/user/:user_id/movies',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de filmes por usuário'
                },
                {
                    'Endpoint': '/api/medias/user/:user_id/games',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de jogos por usuário'
                },
                {
                    'Endpoint': '/api/medias/user/:user_id/books',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de livros por usuário'
                },
                {
                    'Endpoint': '/api/medias/goal/:goal_id',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': None,
                    'description': 'GET: Retorna todos os registros de mídias por meta'
                },
            ],
            "ranking": [
                {
                    'Endpoint': '/api/ranking',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {},
                    'description': 'GET: Retorna um array com um ranking geral'
                },
                {
                    'Endpoint': '/api/ranking/:media_type',
                    'method': 'GET',
                    'headers': {"Authorization": "Bearer token"},
                    'body': {},
                    'description': 'GET: Retorna um array com um ranking geral por categoria (movies / games / books)'
                }
            ]
        }
    ]

    providers = ['google']

    def get_routes():
        return Response(Utils.routes)


class UserUtils:

    def get_me(request):
        current_user = request.user
        user = User.objects.filter(id=current_user.id).first()
        if user is None:
            return Response(data={"error": "Nenhum usuário logado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user, many=False)     
        return Response(serializer.data)

    def get_all_users():
        users = User.objects.all().order_by('first_name', 'last_name')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def get_user_by_id(request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, many=False)
        except:
            return Response(data={"error": "Nenhum usuário encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    def get_user_by_username_or_email(request, username):
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.filter(email=username).first()

        if user is not None:
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            return Response(data={"error": "Nenhum usuário encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def create_user(request):
        data = request.data
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        provider = data['provider']
        image_url = data['image_url']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_email:
            return Response(data={"error": "Email já cadastrado"}, status=status.HTTP_401_UNAUTHORIZED)

        if user_by_username:
            return Response(data={"error": "Username já cadastrado"}, status=status.HTTP_401_UNAUTHORIZED)

        if (provider in Utils.providers):
            password = password + f"_[{provider}]"

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        userinfo = UserInfo.objects.create(
            user_id = user.id,
            provider=provider,
            image_url=image_url
        )
        userinfo.save()
        login_auth(request, user)

        serialized_user = UserUtils.generate_user_token(request)
        return Response(serialized_user)

    def update_user(request, user_id):
        data = request.data
        current_user = request.user
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user_id=user_id)

        if (str(current_user) == str(user.username)):
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.set_password(data['password'])
            userinfo.image_url = data['image_url']
            user.save()
            userinfo.save()
            login_auth(request, user)
        else:
            return Response(data={"error": "Usuário diferente do Usuário em sessão"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def delete_user(request, user_id):
        deleted_user = str(request.user)
        current_user = request.user
        user = User.objects.get(id=user_id)

        if (str(current_user) == str(user.username)):
            user.delete()
        else:
            return Response(data={"error": "Usuário diferente do Usuário em sessão"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={"msg": f"{deleted_user} foi deletado"}, status=status.HTTP_200_OK)

    def login(request):
        data = request.data
        username = data['username']
        password = data['password']
        provider = data['provider']
        if provider in Utils.providers:
            password = password + f"_[{provider}]"

        user = authenticate(username=username, password=password)

        if user is None:
            user_by_email = User.objects.filter(email=username).first()

            if user_by_email is not None:
                username_email = user_by_email.username
                user = authenticate(username=username_email, password=password)

                if user is None:
                    return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)        
        
        login_auth(request, user)
        serialized_user = UserUtils.generate_user_token(request)

        return Response(serialized_user)

    def logout(request):
        prev_user = str(request.user.username)
        logout_auth(request)
        return Response(data={"msg": f"{prev_user} deslogado"}, status=status.HTTP_200_OK)
        
    def generate_user_token(request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        refresh = RefreshToken.for_user(user)
                
        token = {
            # 'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        serialized_user = {
            'id': serializer.data['id'],
            'username': serializer.data['username'],
            'first_name': serializer.data['first_name'],
            'last_name': serializer.data['last_name'],
            'email': serializer.data['email'],
            'last_login': serializer.data['last_login'],
            'date_joined': serializer.data['date_joined'],
            'userinfo': serializer.data['userinfo'],
            'token': token['access']
        }

        return serialized_user


class MediaTypeUtils:
    def get_all_media_type():
        media_types = MediaType.objects.all().order_by('id')
        serializer = MediaTypeSerializer(media_types, many=True)
        return Response(serializer.data)


class GoalUtils:
    def get_all_goals(mediatype_id, is_active):
        goals = Goal.objects.all().order_by('-start_date')

        if mediatype_id > 0:
            goals = goals.filter(mediatype_id=mediatype_id).order_by(
                '-start_date', '-is_active')

        if is_active > 0:
            if is_active == 1:
                goals = goals.filter(is_active=True).order_by(
                    '-start_date', '-is_active')
            elif is_active == 2:
                goals = goals.filter(is_active=False).order_by(
                    '-start_date', '-is_active')
            else:
                goals = goals.filter(is_done=True).order_by(
                    '-start_date', '-is_active')

        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    def get_goal_by_id(request, goal_id):
        try:
            goal = Goal.objects.get(id=goal_id)
            serializer = GoalSerializer(goal, many=False)
        except:
            return Response(data={"error": "Nenhuma meta encontrada"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    def get_all_goals_by_user(request, mediatype_id, is_active, user_id):
        goals = Goal.objects.filter(user_id=user_id).order_by('-start_date')

        if mediatype_id > 0:
            goals = goals.filter(mediatype_id=mediatype_id).order_by(
                '-start_date', '-is_active')

        if is_active > 0:
            if is_active == 1:
                goals = goals.filter(is_active=True).order_by(
                    '-start_date', '-is_active')
            elif is_active == 2:
                goals = goals.filter(is_active=False).order_by(
                    '-start_date', '-is_active')
            else:
                goals = goals.filter(is_done=True).order_by(
                    '-start_date', '-is_active')

        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    def create_goal(request):
        data = request.data
        user = request.user
        user_id = user.id

        mediatype_id = data['mediatype']
        mediatype = MediaType.objects.get(id=mediatype_id)

        creator_id = data['creator']
        if creator_id == "":
            creator_id = user.id
        creator = User.objects.get(id=creator_id)

        objective_quantity = data['objective_quantity']
        current_quantity = 0

        limit_days = data['limit_days']
        limit_date = date.today() + timedelta(days=int(limit_days))

        is_active = True
        is_done = False

        active_goal_by_type = Goal.objects.filter(
            mediatype=mediatype, is_active=True, user_id=user_id).first()

        if active_goal_by_type:
            return Response(data={"error": "Já existe uma meta ativa para esta categoria"}, status=status.HTTP_401_UNAUTHORIZED)

        goal = Goal.objects.create(
            user=user,
            mediatype=mediatype,
            creator=creator,
            objective_quantity=objective_quantity,
            current_quantity=current_quantity,
            limit_date=limit_date,
            is_active=is_active,
            is_done=is_done
        )
        goal.save()

        serializer = GoalSerializer(goal, many=False)
        return Response(serializer.data)

    def delete_goal(request, goal_id):
        goal = Goal.objects.get(id=goal_id)
        goal.delete()
        return Response(data={"msg": "Meta deletada"}, status=status.HTTP_200_OK)


class FavoriteGoalsUtils:

    def get_all_favorite_goals(request):
        goals = Goal.objects.raw(
            "SELECT " +
            "   api_goal.id, api_goal.objective_quantity, (api_goal.limit_date - api_goal.start_date) as limit_days, api_goal.mediatype_id, creator_id, count(api_favoritegoals.goal_id) as likes " +
            "FROM " +
            "   api_goal " +
            "INNER JOIN api_favoritegoals ON api_favoritegoals.goal_id = api_goal.id " +
            "GROUP BY " +
            "   api_goal.id " +
            "ORDER BY " +
            "   count(api_favoritegoals.goal_id) desc "
        )

        serializer = GoalTemplateSerializer(goals, many=True)
        for i, data in enumerate(serializer.data):
            limit_date = datetime.strptime(data['limit_date'], '%Y-%m-%d').date()
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            limit_days = (limit_date - start_date).days
            data['limit_days'] = limit_days
            data['likes'] = goals[i].likes
        
        return Response(serializer.data)

    def get_all_favorite_goals_by_user(request, user_id):
        goals = Goal.objects.raw(
            "SELECT " +
            "   api_goal.id, api_goal.objective_quantity, (api_goal.limit_date - api_goal.start_date) as limit_days, api_goal.mediatype_id, creator_id " +
            "FROM " +
            "   api_goal " +
            "INNER JOIN api_favoritegoals ON api_favoritegoals.goal_id = api_goal.id " +
            "WHERE " +
            "   api_favoritegoals.user_id = %s",
            [user_id]
        )

        serializer = GoalTemplateSerializer(goals, many=True)
        for data in serializer.data:
            limit_date = datetime.strptime(data['limit_date'], '%Y-%m-%d').date()
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            limit_days = (limit_date - start_date).days
            data['limit_days'] = limit_days
        
        return Response(serializer.data)

    def create_or_delete_favorite_goal(request):
        data = request.data
        user = request.user

        user_id = user.id
        goal_id = data['goal']

        goal_like = FavoriteGoals.objects.filter(
            user_id=user_id, goal_id=goal_id).first()

        if goal_like is None:
            goal_like = FavoriteGoals.objects.create(
                user_id=user_id,
                goal_id=goal_id
            )
            goal_like.save()

        else:
            goal_like.delete()
            return Response(data={"msg": f"Meta retirada das favoritas"}, status=status.HTTP_200_OK)

        serializer = FavoriteGoalsSerializer(goal_like, many=False)
        return Response(serializer.data)

class MediaUtils:
    def get_all_medias(mediatype_id):
        medias = Media.objects.all().order_by('-register_date')

        if mediatype_id > 0:
            medias = medias.filter(mediatype_id=mediatype_id).order_by(
                '-register_date')

        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)

    def get_media_by_id(request, media_id):
        try:
            media = Media.objects.get(id=media_id)
            serializer = MediaSerializer(media, many=False)
        except:
            return Response(data={"error": "Nenhuma meta encontrada"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    def get_all_medias_by_user(request, mediatype_id, user_id):
        medias = Media.objects.filter(user_id=user_id).order_by('-register_date')

        if mediatype_id > 0:
            medias = medias.filter(mediatype_id=mediatype_id).order_by(
                '-register_date')

        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)
    
    def get_all_medias_by_goal(request, goal_id):
        medias = Media.objects.filter(goal_id=goal_id).order_by('-register_date')

        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)

    def create_media(request):
        data = request.data
        user = request.user
        user_id = user.id

        mediatype_id = data['mediatype']
        id_on_api = data['id_on_api']
        image_on_api = data['image_on_api']

        mediatype = MediaType.objects.get(id=mediatype_id)
        active_goal_by_type = Goal.objects.filter(mediatype=mediatype, is_active=True, user_id=user_id).first()

        if active_goal_by_type is not None:
            objective_quantity = active_goal_by_type.objective_quantity
            current_quantity = active_goal_by_type.current_quantity + 1
            is_active = active_goal_by_type.is_active
            is_done = active_goal_by_type.is_done
            limit_date = active_goal_by_type.limit_date

            if current_quantity >= objective_quantity:
                end_date = date.today()
                is_active = False
                if date.today() <= limit_date:
                    is_done = True
            
            active_goal_by_type.current_quantity = current_quantity
            active_goal_by_type.is_active = is_active
            active_goal_by_type.is_done = is_done            
            if not is_active:
                active_goal_by_type.end_date = end_date
            active_goal_by_type.save()            

        media = Media.objects.create(
            user=user,
            mediatype=mediatype,
            goal=active_goal_by_type,
            id_on_api=id_on_api,
            image_on_api=image_on_api
        )
        media.save()

        serializer = MediaSerializer(media, many=False)
        return Response(serializer.data)

    # def delete_goal(request, goal_id):
    #     goal = Goal.objects.get(id=goal_id)
    #     goal.delete()
    #     return Response(data={"msg": "Meta deletada"}, status=status.HTTP_200_OK)

class RankingUtils:

    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_ranking(request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT SUM(points) as points, user_id FROM ( " +
                "   (select " +
                "       count(id) as points, user_id " +
                "   from " +
                "       api_media " +
                "   group by user_id) " +
                "   union " +
                "   (select " +
                "       sum(current_quantity) as points, user_id " +
                "   from " +
                "       api_goal " +
                "   where is_done = true " +
                "   group by user_id) " +
                "   union " +
                "   (select " +
                "       sum(current_quantity)*0.5 as undone_goal_points, user_id " +
                "   from " +
                "       api_goal "+
                "   where is_done = false and is_active = false " +
                "   group by user_id) " +
                ") as points_table " +
                "group by user_id " + 
                "order by points desc "
            )
            result = RankingUtils.dictfetchall(cursor)

        print(result)
        return Response(result)

    def get_ranking_by_type(request, mediatype_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT SUM(points) as points, user_id FROM ( " +
                "   (select " +
                "       count(id) as points, user_id " +
                "   from " +
                "       api_media " +
                "   where mediatype_id = %s " +
                "   group by user_id) " +
                "   union " +
                "   (select " +
                "       sum(current_quantity) as points, user_id " +
                "   from " +
                "       api_goal " +
                "   where is_done = true and mediatype_id = %s " +
                "   group by user_id) " +
                "   union " +
                "   (select " +
                "       sum(current_quantity)*0.5 as undone_goal_points, user_id " +
                "   from " +
                "       api_goal "+
                "   where is_done = false and is_active = false and mediatype_id = %s " +
                "   group by user_id) " +
                ") as points_table " +
                "group by user_id " + 
                "order by points desc ", 
                [mediatype_id, mediatype_id, mediatype_id]
            )
            result = RankingUtils.dictfetchall(cursor)

        print(result)
        return Response(result)
