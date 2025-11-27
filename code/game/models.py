from django.db import models
from joystickjuice.utils import STATUS_CHOICES
from django.conf import settings

class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    synopsis = models.TextField()
    developer = models.CharField(max_length=100)
    cover_url = models.URLField(max_length=200, blank=True, null=True)
    banner_url = models.URLField(max_length=200, blank=True, null=True)
    trailer_url = models.URLField(max_length=200, blank=True, null=True)

class UserGameList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FavoriteGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class LikeGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)