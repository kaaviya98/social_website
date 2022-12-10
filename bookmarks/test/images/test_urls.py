from django.test import TestCase
from django.urls import reverse, resolve
from images.views import image_create, image_detail, image_like


class ImageUrls(TestCase):
    def test_image_create_url(self):
        self.assertEqual(
            (resolve(reverse("images:create")).func), image_create
        )

    def test_image_detail_url(self):
        self.assertEqual(
            (resolve(reverse("images:detail", args=[1, "some_slug"])).func),
            image_detail,
        )

    def test_image_like_url(self):
        self.assertEqual((resolve(reverse("images:like")).func), image_like)
