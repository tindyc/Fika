from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import FriendRequest
import json

# Create your views here.
def friend_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = User.objects.filter(username__startswith=search_query)
            accounts = [] # [(account, true), (account1, false)...]
            for account in search_results:
                accounts.append((account, False)) # Hardcode, to be corrected
            
            context["accounts"] = accounts

    return render(request, "friend/search_results.html", context)


def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(id=user_id)
			try:
				# Get any friend requests
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a friend request.")
					# If not active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")
