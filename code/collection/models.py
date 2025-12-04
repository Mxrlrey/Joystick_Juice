from django.db import models
from django.conf import settings
from game.models import Game  # assumindo app game.Game

User = settings.AUTH_USER_MODEL

class GameList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_lists")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.owner}"

class GameListItem(models.Model):
    list = models.ForeignKey(GameList, on_delete=models.CASCADE, related_name="items")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    note = models.CharField(max_length=200, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('list', 'game')
        ordering = ['order', '-added_at']

    def __str__(self):
        return f"{self.game} in {self.list}"