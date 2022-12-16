from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from bookmarks.common.decorators import ajax_required, is_ajax
from django.views.generic import ListView
from actions.utils import create_action


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, "bookmarked image", new_item)
            messages.success(request, "Image added successfully")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )


class ImageListView(ListView):
    model = Image
    paginate_by = 6
    context_object_name = "images"

    def get_template_names(self):
        template_name = "images/image/list.html"
        if is_ajax(self.request):
            template_name = "images/image/list_ajax.html"
        return template_name


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image},
    )


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
                response = JsonResponse({"status": "ok"})
            return response
        except Exception:
            pass
    return JsonResponse({"status": "error"})
