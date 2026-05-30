from rest_framework import filters, viewsets

from game.models import Game
from review.models import Comment, Review

from .serializers import CommentSerializer, GameSerializer, ReviewSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('title')
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre', 'developer']
    ordering_fields = ['title', 'release_date', 'developer']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['game__title', 'user__username', 'comment']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        return Review.objects.select_related('game', 'user').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['review__game__title', 'user__username', 'opinion']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Comment.objects.select_related('review', 'review__game', 'user').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
