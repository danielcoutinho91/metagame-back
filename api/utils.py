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
                'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha", "provider": ""},
                'description': 'GET: Retorna um array com todos os usuários do sistema, POST: Cria um novo usuário com os dados da requisição'
            },
            {
                'Endpoint': '/api/user/:id',
                'method': 'GET, PUT',
                'body': {"username": "name", "email": "user_email@email.com", "first_name": "First", "last_name": "Last", "password": "senha"},
                'description': 'GET: Retorna o usuário pelo id especificado, PUT: Atualiza o usuário com o id especificado'
            },   
            {
                'Endpoint': '/api/user/find/:username_or_email',
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
            return Response(data={"error": "Nenhum usuário encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)
    
    def get_user_by_username_or_email(request, pk):
        user = User.objects.filter(username=pk).first()
        if user is None:
            user = User.objects.filter(email=pk).first()
        
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

        if (provider=='google'):
            password=username + "_google"          
        
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
            return Response(data={"error": "Usuário diferente do Usuário em sessão"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)
  
    def delete_user(request, pk):
        deleted_user = str(request.user)
        current_user = request.user
        user = User.objects.get(id=pk)

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
            password = username + "_google"
            
        user = authenticate(username=username, password=password)

        if user is not None:
            login_auth(request, user)
            return Response(data={"msg": f"{request.user} autenticado"}, status=status.HTTP_200_OK)

        else:
            user_by_email = User.objects.filter(email=username).first()            
            if user_by_email is not None:
                username_email = user_by_email.username
                user = authenticate(username=username_email, password=password)
                if user is not None:
                    login_auth(request, user)
                    return Response(data={"msg": f"{user.username} autenticado"}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(data={"error": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def logout(request):
        prev_user = str(request.user.username)
        logout_auth(request)
        return Response(data={"msg": f"{prev_user} deslogado"}, status=status.HTTP_200_OK)