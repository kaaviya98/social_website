from django.test import TestCase
from django.urls import reverse, resolve
from images.views import image_create


class ImageUrls(TestCase):
    def test_image_create_url(self):
        self.assertEqual(
            (resolve(reverse("images:create")).func), image_create
        )
