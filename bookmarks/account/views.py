from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def authorize_user(user, request):
    if user.is_active:
        login(request, user)
        response = HttpResponse("Authenticated successfully")
    else:
        response = HttpResponse(
            "Account has been disabled please try any other account"
        )
    return response


def authenticate_user(request):

    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            response = authorize_user(user, request)
        else:
            response = HttpResponse("Invalid login")
    return response


def user_login(request):

    if request.method == "POST":
        response = authenticate_user(request=request)
    else:
        response = render(request, "account/login.html", {"form": LoginForm()})
    return response
