from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("add", views.fetch_and_save, name="add_game"),
    path("list", views.list_games, name="list_game"),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/add/<int:game_id>/', views.add_to_list, name='add_to_list'),
    path('game/update/<int:game_id>/', views.update_game_status, name='update_game_status'),
    path('game/remove/<int:game_id>/', views.remove_from_list, name='remove_from_list'),
    path("game/<int:game_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("game/<int:game_id>/like/", views.toggle_like, name="toggle_like"),
]