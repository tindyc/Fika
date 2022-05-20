from django.urls import path
from . import views

urlpatterns = [
    path("login", views.member_login, name="login"),
    path("logout", views.member_logout, name="logout"),
]
