from django.urls import path
from . import views

urlpatterns = [
    path('<int:game_id>/create/', views.create_review, name='create_review'),
    path('<int:game_id>/reviews/', views.list_reviews, name='list_reviews'),
    path('detail/<int:pk>/', views.review_detail, name='detail_review'),
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('<int:review_id>/comment/', views.create_comment, name='create_comment'),
    path('<int:review_id>/comments/', views.comment_list, name='comment_list'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]