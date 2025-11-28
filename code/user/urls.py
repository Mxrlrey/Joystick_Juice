from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup, name="account_signup"),
    path("users/admin/", views.list_, name="account_user_list"),
    path("users/<int:user_id>/", views.detail_admin, name="account_detail_admin"), 
    path("user/", views.detail_self, name="account_detail_self"),
    path("edit/profile", views.edit_profile, name="account_edit_profile"),
    path("edit/avatar/", views.edit_avatar, name="account_edit_avatar"),
    path("delete/", views.delete, name="account_delete_user"),
]
