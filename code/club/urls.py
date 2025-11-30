from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_club, name='create_club'),
    path('list/', views.list_clubs, name='list_clubs'),
    path('<int:club_id>/edit/', views.edit_club, name='edit_club'),
    path('<int:club_id>/delete/', views.delete_club, name='delete_club'),
    path('<int:club_id>/join/', views.join_club, name='join_club'),
    path("<int:club_id>/chat/", views.club_chat, name="club_chat"),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('user/<int:user_id>/clubs/', views.list_user_clubs, name='list_user_clubs'),
    path('<int:club_id>/leave/', views.leave_club, name='leave_club'),
]