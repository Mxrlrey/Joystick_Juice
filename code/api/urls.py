from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GameViewSet, ReviewViewSet


router = DefaultRouter()
router.register('games', GameViewSet, basename='api-games')
router.register('reviews', ReviewViewSet, basename='api-reviews')
router.register('comments', CommentViewSet, basename='api-comments')

urlpatterns = [
    path('', include(router.urls)),
]
