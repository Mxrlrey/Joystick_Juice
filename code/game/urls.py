from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("add", views.fetch_and_save, name="add_game"),
    path("list", views.list_games, name="list_game"),
    path("<int:game_id>/", views.game_detail, name="game_detail"), #feito por gabriel, consulte ele
]