from django.db import models
from django.contrib.auth.models import User
from game.models import Game

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField("Nota", max_digits=2, decimal_places=1)
    comment = models.TextField("Comentário")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} avaliou {self.game.title} ({self.rating}/5)"
    
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.TextField("Opinião")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comentou na review de {self.review}"