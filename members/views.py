from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterUserForm


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

    return render(request, "member/member_profile.html", context)