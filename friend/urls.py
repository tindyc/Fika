from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.friend_search_view, name="search"),
    path("friend_request/", views.send_friend_request, name="friend-request"),
    path("friend_request/<user_id>", views.friend_requests_view, name="friend-requests"),
    path("friend_list/<user_id>", views.friends_list_view, name="friends-list"),
    path("accept_friend_request/<friend_request_id>", views.accept_friend_request, name="accept-friend-request"),
    path("decline_friend_request/<friend_request_id>", views.decline_friend_request, name="decline-friend-request"),
    path("cancel_friend_request/", views.cancel_friend_request, name="cancel-friend-request"),
    path("remove_friend/", views.remove_friend, name="remove-friend"),
]
