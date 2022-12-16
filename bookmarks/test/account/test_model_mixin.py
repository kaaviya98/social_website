from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile
from images.models import Image


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="johnpassword"
        )
        Profile.objects.create(user=self.user)

    def create_images(self, count):
        images = []
        for _ in range(count):
            image = Image.objects.create(
                user=self.user,
                title="test",
                slug="test",
                image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            )
            images.append(image)
        return images
