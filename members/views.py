from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from friend.friend_request_status import FriendRequestStatus

from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from .forms import RegisterUserForm, UpdateUserForm


def member_login(request):
    """Renders login page or logins the user depending on req. method"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("home")
        else:
            # Return an 'invalid login' error message.
            messages.warning(
                request,
                ("Invalid login, check your username & password before trying again."),
            )
            return redirect("login")

    return render(request, "authenticate/login.html", {})

@login_required(login_url="/members/login")
def member_logout(request):
    logout(request)
    messages.success(request, ("Logout was successful!"))
    return redirect("home")


def member_registration(request):
    """Registers new user accounts"""
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            form.save()
            # Clean the form data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # Auth user using clean data
            user = authenticate(username=username, password=password)
            # Login newly registered user
            login(request, user)
            # Success Message
            messages.success(request, ("Registration Successful!"))

            return redirect("home")
    else:
        # Create empty form on req. method GET
        form = RegisterUserForm()

    return render(request, "authenticate/register_user.html", {"form": form})

@login_required(login_url="/members/login")
def member_profile(request, *args, **kwargs):
    """
        is_self (boolean)
        is_friend (boolean)
            -1: NO_REQUEST_SENT
            0: THEY_SENT_TO_YOU
            1: YOU_SENT_TO_THEM
    """

    context = {
        "user": request.user
    }

    user_id = kwargs.get("user_id")

    try:
        account = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    
    if account:

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context["friends"] = friends

        # Define state template var.
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        user = request.user
        if user != account:
            context["account"] = account
            is_self = False
            if friends.filter(id=user.id):
                is_friend = True
            else:
                # CASE1: Req. has been sent from them to you 
                is_friend = False
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEY_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: You have sent the friend req. to them
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE3: No request has been sent.
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
        
        context["is_self"] = is_self
        context["is_friend"] = is_friend
        context["BASE_URL"] = settings.BASE_URL
        context["request_sent"] = request_sent
        context["friend_request"] = friend_requests
        context["user_id"] = user_id

        return render(request, "members/member_profile.html", context)


@login_required(login_url="/members/login")
def member_edit(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        # Check if form is valid
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile is updated successfully!")
            return redirect("profile")
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, "members/member_edit.html", {"user_form": user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "members/change_password.html"
    success_message = "Successfully changed your password!"
    success_url = reverse_lazy("profile")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "authenticate/reset_password.html"
    email_template_name = "authenticate/email_reset_password.html"
    subject_template_name = "authenticate/password_reset_subject"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("home")
