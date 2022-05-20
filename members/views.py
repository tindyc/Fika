from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
