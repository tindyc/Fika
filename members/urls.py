from django.urls import path
from . import views

urlpatterns = [
    path("login", views.member_login, name="login"),
    path("logout", views.member_logout, name="logout"),
    path("register", views.member_registration, name="register"),
    path("profile", views.member_profile, name="profile"),
    path("profile_edit", views.member_edit, name="profile_edit"),
]
