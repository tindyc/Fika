from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.friend_search_view, name="search"),
]
