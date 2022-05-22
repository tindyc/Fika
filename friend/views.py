from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import FriendRequest
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required(login_url="/members/login")
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


@login_required(login_url="/members/login")
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

@login_required(login_url="/members/login")
def friend_requests_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		account = User.objects.get(id=user_id)
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("You can't view another users friend requests.")
	else:
		redirect("login")
	return render(request, "friend/friend_requests.html", context)


@login_required(login_url="/members/login")
def accept_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(id=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now accept it
					updated_notification = friend_request.accept()
					payload['response'] = "Friend request accepted."

				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to accept."
		else:
			payload['response'] = "Unable to accept that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")