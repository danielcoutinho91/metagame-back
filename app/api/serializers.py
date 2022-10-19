from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SlugRelatedField
from django.contrib.auth.models import User
from .models import MediaType, Goal, FavoriteGoals, UserInfo

class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['provider', 'image_url']

class UserSerializer(ModelSerializer):
    userinfo = UserInfoSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'userinfo']

class MediaTypeSerializer(ModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'

class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class GoalTemplateSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'objective_quantity', 'limit_date', 'start_date', 'mediatype_id', 'creator_id']

class FavoriteGoalsSerializer(ModelSerializer):
    class Meta:
        model = FavoriteGoals
        fields = '__all__'