from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import MediaType, Goal, FavoriteGoals

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MediaTypeSerializer(ModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'

class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class FavoriteGoalsSerializer(ModelSerializer):
    class Meta:
        model = FavoriteGoals
        fields = '__all__'