from django.urls import path
from . import views

urlpatterns = [
    path('<int:game_id>/create/', views.create_review, name='create_review'),
    path('<int:game_id>/reviews/', views.list_reviews, name='list_reviews'),
    path('detail/<int:pk>/', views.review_detail, name='detail_review'),
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
]