# collection/urls.py
from django.urls import path
from . import views


urlpatterns = [
    # toggle rápido de favoritos (ex: /collections/favorites/toggle/12/)
    path('favorites/toggle/<int:game_id>/', views.quick_toggle_favorite, name='toggle_favorite'),

    # CRUD de listas (nomes compatíveis com os redirects nas views)
    path('', views.list_lists, name='list_list'),                      # listar listas  (redirect: 'list_list')
    path('create/', views.create_list, name='create_list'),            # criar lista
    path('<int:pk>/', views.list_detail, name='list_detail'),          # ver detalhes da lista (redirect: 'list_detail')
    path('<int:pk>/edit/', views.edit_list, name='edit_list'),         # editar lista
    path('<int:pk>/delete/', views.delete_list, name='delete_list'),   # deletar lista

    # CRUD de itens (views usam list_pk / item_pk)
    path('<int:list_pk>/add/', views.add_item, name='add_item'),                       # adiciona item via POST
    path('<int:list_pk>/item/<int:item_pk>/edit/', views.edit_item, name='edit_item'), # editar item
    path('<int:list_pk>/item/<int:item_pk>/remove/', views.remove_item, name='remove_item'), # remover item
]
