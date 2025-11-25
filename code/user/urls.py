from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("", views.edit_profile, name="edit_profile"),
    path("avatar", views.edit_avatar, name="edit_avatar"),
]