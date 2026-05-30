from django.contrib.auth import get_user_model
from rest_framework import serializers

from game.models import Game
from review.models import Comment, Review


User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GameSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    favorites_count = serializers.IntegerField(source='favorites.count', read_only=True)

    class Meta:
        model = Game
        fields = [
            'id',
            'title',
            'genre',
            'release_date',
            'synopsis',
            'developer',
            'cover_url',
            'banner_url',
            'trailer_url',
            'likes_count',
            'favorites_count',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'game', 'game_title', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'opinion', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
