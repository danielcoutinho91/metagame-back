from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class UserTestCase(TestCase):

    def test_create_user(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        response = client.post('/api/users', data, format='json')
        self.assertEquals(response.status_code, 200)
    
    def test_get_all_users(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        response = client.get('/api/users')
        self.assertEquals(response.status_code, 200)

    def test_get_user_by_id(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id
        response = client.get(f'/api/users/{user_id}')
        self.assertEquals(response.status_code, 200)

    def test_get_me(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        response = client.get('/api/me')
        self.assertEquals(response.status_code, 200)
    
    def test_get_user_by_username(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        username = user.username
        response = client.get(f'/api/users/find/{username}')
        self.assertEquals(response.status_code, 200)
    
    def test_get_user_by_email(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        email = user.email
        response = client.get(f'/api/users/find/{email}')
        self.assertEquals(response.status_code, 200)

    def test_login(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        data_login = {"username": "test_user", "password": "test", "provider": ""}
        response = client.post('/api/login', data_login, format='json')
        self.assertEquals(response.status_code, 200)
    
