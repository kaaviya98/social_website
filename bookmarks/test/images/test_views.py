from django.test import TestCase
from django.urls import reverse
from images.models import Image
from test.account.test_model_mixin import ModelMixinTestCase


class ImageCreateView(ModelMixinTestCase, TestCase):
    def test_template_used_with_image_create(self):

        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("images:create"))

        self.assertTemplateUsed(response, "images/image/create.html")

    def test_create_image_adds_new_image_to_database(self):
        self.client.login(username="john", password="johnpassword")

        self.client.post(
            reverse("images:create"),
            data={
                "title": "test-image",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        self.assertTrue(Image.objects.filter(user=self.user).exists())
