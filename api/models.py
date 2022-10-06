from django.db import models
from django.contrib.auth.models import User

class TipoMidia(models.Model):
    tipo = models.CharField(max_length=30)

class Meta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipomidia = models.ForeignKey(TipoMidia, on_delete=models.CASCADE)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criador')
    quantidade_objetivo = models.BigIntegerField()
    quantidade_atual = models.BigIntegerField()
    data_inicio = models.DateField(auto_now_add=True)
    data_limite = models.DateField()
    data_conclusao = models.DateField(blank=True, null=True)
    is_ativa = models.BooleanField()
    is_cumprida = models.BooleanField()

