from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    user_form = UserRegistrationForm(data=request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data["password"])
        new_user.save()
        return render(
            request, "account/register_done.html", {"new_user": new_user}
        )

    return render(
        request, "account/register.html", {"form": UserRegistrationForm}
    )
