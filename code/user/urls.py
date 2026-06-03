from django.urls import path

from .views import (
    AccountAvatarUpdateView,
    AccountDeleteView,
    AccountDetailView,
    AccountProfileUpdateView,
    SignupView,
)

urlpatterns = [
    path('signup', SignupView.as_view(), name='account_signup'),
    path('users/<int:user_id>', AccountDetailView.as_view(), name='account_detail_admin'),
    path('me', AccountDetailView.as_view(), name='account_detail_self'),
    path('edit/profile', AccountProfileUpdateView.as_view(), name='account_edit_profile'),
    path('edit/avatar/', AccountAvatarUpdateView.as_view(), name='account_edit_avatar'),
    path('delete', AccountDeleteView.as_view(), name='account_delete_user'),
]
