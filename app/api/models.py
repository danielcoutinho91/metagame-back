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

class FavoriteGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    provider = models.CharField(max_length=30)
    image_url = models.CharField(max_length=300)

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, blank=True, null=True)
    mediatype = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    id_on_api = models.CharField(max_length=300)
    image_on_api = models.TextField()
    register_date = models.DateField(auto_now_add=True)
