from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
def member_profile(request):
    context = {
        "user": request.user
    }

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