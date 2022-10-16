from django.db import models
from django.contrib.auth.models import User

class MediaType(models.Model):
    type = models.CharField(max_length=30)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mediatype = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    objective_quantity = models.BigIntegerField()
    current_quantity = models.BigIntegerField()
    start_date = models.DateField(auto_now_add=True)
    limit_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField()
    is_done = models.BooleanField()