from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer

class Utils:
    routes = [
        {"user": [
            {
                'Endpoint': '/api',
                'method': 'GET',
                'body': None,
                'description': 'Retorna um array routes'
            },
            {
                'Endpoint': '/api/user',
                'method': 'GET, POST',
                'body': {"username": "aaaaaa", "email": "aaaaaa@aaa.com", "first_name": "Aaaaaa", "last_name": "Aaaaaa", "password": "aaaaaa"},
                'description': 'GET: Retorna um array com todos os usuários do sistema, POST: Cria um novo usuário com os dados da requisição'
            },
            {
                'Endpoint': '/api/user/:id',
                'method': 'GET, PUT',
                'body': {"username": "aaaaaa", "email": "aaaaaa@aaa.com", "first_name": "Aaaaaa", "last_name": "Aaaaaa", "password": "aaaaaa"},
                'description': 'GET: Retorna o usuário pelo id especificado, PUT: Atualiza o usuário com o id especificado'
            },        
            {
                'Endpoint': '/api/login',
                'method': 'POST',
                'body': {"username": "aaaaaa", "password": "aaaaaa"},
                'description': 'Faz login do usuário com dados enviados através de uma requisição POST'
            },
            {
                'Endpoint': '/api/logout',
                'method': 'POST',
                'body': None,
                'description': 'Faz logout do usuário'
            },
            ]
        }
    ]

    def get_routes():
        return Response(Utils.routes)

class UserUtils:   

    def get_all_users():
        users = User.objects.all().order_by('first_name', 'last_name')        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def get_user_by_id(request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)
    
    def create_user(request):
        data = request.data
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username:
            return HttpResponse("Já existe um usuário com esse nome")

        if user_by_email:
            return HttpResponse("Email já cadastrado")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
    def update_user(request, pk):
        data = request.data
        current_user = request.user
        user = User.objects.get(id=pk)

        if (str(current_user) == str(user.username)):
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.set_password(data['password'])
            user.save()
            
        else:
            return HttpResponse("Usuário diferente")
        
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)
  
    def delete_user(request, pk):
        deleted_user = str(request.user)
        current_user = request.user
        user = User.objects.get(id=pk)

        if (str(current_user) == str(user.username)):
            user.delete()

        else:
            return HttpResponse("Usuário diferente")
        return Response(f"{deleted_user} foi deletado!")
    
    def login(request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login_auth(request, user)
            return HttpResponse(f"{request.user} autenticado")

        else:
            user_by_email = User.objects.filter(email=username).first()            
            if user_by_email is not None:
                username_email = user_by_email.username
                user = authenticate(username=username_email, password=password)
                if user is not None:
                    login_auth(request, user)
                    return HttpResponse("Autenticado")
                else:
                    return HttpResponse("Usuário ou senha inválidos")
            else:
                return HttpResponse("Usuário ou senha inválidos")
    
    def logout(request):
        prev_user = str(request.user.username)
        logout_auth(request)
        return HttpResponse(f"{prev_user} deslogado")