from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def member_login(request):
    return render(request, "authenticate/login.html", {})
