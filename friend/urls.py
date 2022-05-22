from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.friend_search_view, name="search"),
    path("friend_request/", views.send_friend_request, name="friend-request"),
    path("friend_request/<user_id>", views.friend_requests_view, name="friend-requests"),
]
