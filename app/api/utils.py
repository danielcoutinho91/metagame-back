from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from datetime import date, datetime, timedelta
from .serializers import UserSerializer, MediaTypeSerializer, GoalSerializer, FavoriteGoalsSerializer, GoalTemplateSerializer
from .models import FavoriteGoals, MediaType, Goal


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
                    'Endpoint': '/api/users',
                    'method': 'GET, POST',
                    'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha", "provider": ""},
                    'description': 'GET: Retorna um array com todos os usuários do sistema, POST: Cria um novo usuário com os dados da requisição'
                },
                {
                    'Endpoint': '/api/users/:user_id',
                    'method': 'GET, PUT, DELETE',
                    'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha"},
                    'description': 'GET: Retorna o usuário pelo id especificado, PUT: Atualiza o usuário com o id especificado, DELETE: Deleta o usuário com o id especificado'
                },
                {
                    'Endpoint': '/api/users/find/:username_or_email',
                    'method': 'GET, PUT',
                    'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha"},
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
                    'body': {"mediatype": "mediatype_id", "creator": "creator_id", "objective_quantity": "10", "limit_days": "30"},
                    'description': 'GET: Retorna um array com todos as metas do sistema, POST: Cria uma nova meta com os dados da requisição'
                },
                {
                    'Endpoint': '/api/goals/:goal_id',
                    'method': 'GET, DELETE',
                    'body': None,
                    'description': 'GET: Retorna a meta pelo id especificao, DELETE: Deleta a meta com o id especificado'
                },
                {
                    'Endpoint': '/api/goals/:is_active',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas pela status dela. (active / inactive / done)'
                },
                {
                    'Endpoint': '/api/goals/:media_type',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas pelo tipo dela. (movies / games / books)'
                },
                {
                    'Endpoint': '/api/goals/favorites',
                    'method': 'GET, POST',
                    'body': None,
                    'description': 'GET: Retorna todas as metas favoritas ordenadas por quantidade de likes. POST: Cria ou remove uma meta favorita'
                },
                {
                    'Endpoint': '/api/goals/:media_type/:is_active',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas pelo tipo e status dela. (movies / games / books) / (active / inactive / done)'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas do usuário.'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/:media_type',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas de determinado tipo do usuário. (movies / games / books)'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/favorites',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas favoritas de determinado tipo do usuário.'
                },
                {
                    'Endpoint': '/api/goals/user/:user_id/:media_type/:is_active',
                    'method': 'GET',
                    'body': None,
                    'description': 'GET: Retorna todas as metas de determinado tipo e status do usuário. (movies / games / books) / (active / inactive / done)'
                },
            ]
        }
    ]

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

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_email:
            return Response(data={"error": "Email já cadastrado"}, status=status.HTTP_401_UNAUTHORIZED)

        if user_by_username:
            return Response(data={"error": "Username já cadastrado"}, status=status.HTTP_401_UNAUTHORIZED)

        if (provider == 'google'):
            username = email
            password = email + "_[google]"

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()
        login_auth(request, user)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def update_user(request, user_id):
        data = request.data
        current_user = request.user
        user = User.objects.get(id=user_id)

        if (str(current_user) == str(user.username)):
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.set_password(data['password'])
            user.save()
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
        if provider == 'google':
            password = username + "_[google]"

        user = authenticate(username=username, password=password)

        if user is not None:
            login_auth(request, user)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)

        else:
            user_by_email = User.objects.filter(email=username).first()
            if user_by_email is not None:
                username_email = user_by_email.username
                user = authenticate(username=username_email, password=password)
                if user is not None:
                    login_auth(request, user)
                    serializer = UserSerializer(user, many=False)
                    return Response(serializer.data)
                else:
                    return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(request):
        prev_user = str(request.user.username)
        logout_auth(request)
        return Response(data={"msg": f"{prev_user} deslogado"}, status=status.HTTP_200_OK)


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
