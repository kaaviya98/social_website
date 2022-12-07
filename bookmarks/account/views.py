from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def authorize_user(user, request):
    if user.is_active:
        login(request, user)
        return HttpResponse("Authenticated successfully")
    else:
        return HttpResponse(
            "Account has been disabled please try any other account"
        )


def authenticate_user(request, user):
    if user is not None:
        return authorize_user(user, request)
    else:
        return HttpResponse("Invalid login")


def user_login(request):

    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        return authenticate_user(request, user)

    return render(request, "account/login.html", {"form": LoginForm()})
