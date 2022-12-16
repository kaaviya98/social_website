from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from django.contrib import messages
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def validate_the_registeration_form(request):
    user_form = UserRegistrationForm(data=request.POST)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data["password"])
        new_user.save()
        Profile.objects.create(user=new_user)
        messages.success(
            request,
            "Registration successful you can login now to your account.",
        )
    else:
        messages.error(
            request, "Unsuccessful registration. Invalid information."
        )
    return render(
        request, "account/register.html", {"form": UserRegistrationForm()}
    )


def register(request):
    if request.method == "POST":
        validate_the_registeration_form(request)
    return render(
        request, "account/register.html", {"form": UserRegistrationForm()}
    )


@login_required
def edit(request):
    user_form = UserEditForm(instance=request.user, data=request.POST or None)
    profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES,
    )
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(
            request,
            "your profile has been updated successfully",
        )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        "account/user/list.html",
        {"section": "people", "users": users},
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        "account/user/detail.html",
        {"section": "people", "user": user},
    )
