from django.urls import path

from .views import (
    AddToListView,
    FetchAndSaveView,
    GameCreateView,
    GameDeleteView,
    GameDetailView,
    GameListView,
    GameUpdateView,
    HomePageView,
    RemoveFromListView,
    ToggleFavoriteView,
    ToggleLikeView,
    UpdateGameStatusView,
    UserGameListView,
)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('list', GameListView.as_view(), name='list_game'),
    path('<int:game_id>/', GameDetailView.as_view(), name='game_detail'),
    path('form/add/', GameCreateView.as_view(), name='create_game'),
    path('form/edit/<int:pk>/', GameUpdateView.as_view(), name='edit_game'),
    path('form/delete/<int:pk>/', GameDeleteView.as_view(), name='delete_game'),
    path('add', FetchAndSaveView.as_view(), name='add_game'),
    path('userlist/<int:pk>/', UserGameListView.as_view(), name='user_game_list'),
    path('mylist/', UserGameListView.as_view(), name='my_game_list'),
    path('game/add/<int:game_id>/', AddToListView.as_view(), name='add_to_list'),
    path('game/update/<int:game_id>/', UpdateGameStatusView.as_view(), name='update_game_status'),
    path('game/remove/<int:game_id>/', RemoveFromListView.as_view(), name='remove_from_list'),
    path('game/<int:game_id>/favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('game/<int:game_id>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('', HomePageView.as_view(), name='home'),
]
