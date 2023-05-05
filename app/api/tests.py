from django.test import TestCase
from django.contrib.auth.models import User
from .models import Goal
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

    def test_update_user(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        data_update = {"username": "new_test_user", "email": "new_test@user.com", "first_name": "Teste", "last_name": "User", "password": "new_test", "provider": "", "image_url": ""}
        
        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id
        response = client.put(f'/api/users/{user_id}', data_update, format='json')
        self.assertEquals(response.status_code, 200)

class GoalTestCase(TestCase):

    def test_create_goal(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id

        goal_data = {"mediatype": "1", "creator": f"{user_id}", "objective_quantity": "10", "limit_days": "30"}        
        response = client.post('/api/goals', goal_data, format='json')
        self.assertEquals(response.status_code, 200)

    def test_get_goal_by_id(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id

        goal_data = {"mediatype": "1", "creator": f"{user_id}", "objective_quantity": "10", "limit_days": "30"}        
        client.post('/api/goals', goal_data, format='json')

        goal = Goal.objects.get(id="2")
        goal_id = goal.id
        response = client.get(f'/api/goals/{goal_id}')
        self.assertEquals(response.status_code, 200)
    
    def test_get_goals_by_user(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id

        goal_data = {"mediatype": "1", "creator": f"{user_id}", "objective_quantity": "10", "limit_days": "30"}        
        client.post('/api/goals', goal_data, format='json')
      
        response = client.get(f'/api/goals/user/{user_id}', data, format='json')
        self.assertEquals(response.status_code, 200)

class MediaTestCase(TestCase):
    def test_create_media(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)

        data = {"mediatype": "1", "id_on_api": "id_on_api", "image_on_api": "image_on_api", "name_on_api": "name_on_api"}
        response = client.post('/api/medias', data, format='json')
        self.assertEquals(response.status_code, 200)
    
    def test_get_medias_by_user(self):
        client = APIClient()
        data = {"username": "test_user", "email": "test@user.com", "first_name": "Teste", "last_name": "User", "password": "test", "provider": "", "image_url": ""}        
        client.post('/api/users', data, format='json')

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        user_id = user.id

        goal_data = {"mediatype": "1", "id_on_api": "id_on_api", "image_on_api": "image_on_api", "name_on_api": "name_on_api"}      
        client.post('/api/medias', goal_data, format='json')
      
        response = client.get(f'/api/medias/user/{user_id}', data, format='json')
        self.assertEquals(response.status_code, 200)
        