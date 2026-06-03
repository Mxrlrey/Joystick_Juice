from django.urls import path

from .views import (
    CommentCreateView,
    CommentDeleteView,
    CommentListView,
    CommentUpdateView,
    ReviewCreateView,
    ReviewDeleteView,
    ReviewDetailView,
    ReviewListView,
    ReviewUpdateView,
)

urlpatterns = [
    path('<int:game_id>/create/', ReviewCreateView.as_view(), name='create_review'),
    path('<int:game_id>/reviews/', ReviewListView.as_view(), name='list_reviews'),
    path('detail/<int:pk>/', ReviewDetailView.as_view(), name='detail_review'),
    path('edit/<int:pk>/', ReviewUpdateView.as_view(), name='edit_review'),
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('<int:review_id>/comment/', CommentCreateView.as_view(), name='create_comment'),
    path('<int:review_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]
