from django.urls import path

from .views import (
    ClubChatView,
    ClubCreateView,
    ClubDeleteView,
    ClubDetailView,
    ClubListView,
    ClubUpdateView,
    JoinClubView,
    LeaveClubView,
    UserClubListView,
)

urlpatterns = [
    path('create/', ClubCreateView.as_view(), name='create_club'),
    path('list/', ClubListView.as_view(), name='list_clubs'),
    path('<int:club_id>/edit/', ClubUpdateView.as_view(), name='edit_club'),
    path('<int:club_id>/delete/', ClubDeleteView.as_view(), name='delete_club'),
    path('<int:club_id>/join/', JoinClubView.as_view(), name='join_club'),
    path('<int:club_id>/chat/', ClubChatView.as_view(), name='club_chat'),
    path('<int:club_id>/', ClubDetailView.as_view(), name='club_detail'),
    path('user/<int:user_id>/clubs/', UserClubListView.as_view(), name='list_user_clubs'),
    path('<int:club_id>/leave/', LeaveClubView.as_view(), name='leave_club'),
]
