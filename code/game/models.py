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

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="favorite_games",
        blank=True
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_games",
        blank=True
    )

    def __str__(self):
        return self.title

class UserGameList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

