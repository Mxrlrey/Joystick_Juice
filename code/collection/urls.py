from django.urls import path

from .views import (
    GameListCreateView,
    GameListDeleteView,
    GameListDetailView,
    GameListItemCreateView,
    GameListItemDeleteView,
    GameListItemUpdateView,
    GameListUpdateView,
    PublicListsView,
    ReorderListView,
    UserListsView,
)

urlpatterns = [
    path('mine/', UserListsView.as_view(), name='user_lists'),
    path('public/', PublicListsView.as_view(), name='public_lists'),
    path('create/', GameListCreateView.as_view(), name='create_list'),
    path('<int:pk>/', GameListDetailView.as_view(), name='list_detail'),
    path('<int:pk>/edit/', GameListUpdateView.as_view(), name='edit_list'),
    path('<int:pk>/delete/', GameListDeleteView.as_view(), name='delete_list'),
    path('<int:list_pk>/add/', GameListItemCreateView.as_view(), name='add_item'),
    path('<int:list_pk>/item/<int:item_pk>/edit/', GameListItemUpdateView.as_view(), name='edit_item'),
    path('<int:list_pk>/item/<int:item_pk>/remove/', GameListItemDeleteView.as_view(), name='remove_item'),
    path('list/<int:list_pk>/reorder/', ReorderListView.as_view(), name='reorder_list'),
]
