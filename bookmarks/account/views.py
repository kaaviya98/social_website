from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def validate_the_registeration_form(request):
    user_form = UserRegistrationForm(data=request.POST)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data["password"])
        new_user.save()
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