from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import TipoMidia, Meta

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TipoMidiaSerializer(ModelSerializer):
    class Meta:
        model = TipoMidia
        fields = '__all__'

class MetaSerializer(ModelSerializer):
    class Meta:
        model = Meta
        fields = '__all__'