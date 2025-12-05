from django.urls import path
from . import views


urlpatterns = [
    path('mine/', views.user_lists, name='user_lists'),        
    path('public/', views.public_lists, name='public_lists'),  
    path('create/', views.create_list, name='create_list'),         
    path('<int:pk>/', views.list_detail, name='list_detail'),       
    path('<int:pk>/edit/', views.edit_list, name='edit_list'),      
    path('<int:pk>/delete/', views.delete_list, name='delete_list'),   
    path('<int:list_pk>/add/', views.add_item, name='add_item'),
    path('<int:list_pk>/item/<int:item_pk>/edit/', views.edit_item, name='edit_item'),
    path('<int:list_pk>/item/<int:item_pk>/remove/', views.remove_item, name='remove_item'),
    path("list/<int:list_pk>/reorder/", views.reorder_list, name="reorder_list"),
]
