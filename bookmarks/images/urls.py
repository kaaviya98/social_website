from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = "images"
urlpatterns = [
    path("create/", views.image_create, name="create"),
    path("", login_required(views.ImageListView.as_view()), name="list"),
    path("detail/<int:id>/<slug:slug>/", views.image_detail, name="detail"),
    path("like/", views.image_like, name="like"),
]
