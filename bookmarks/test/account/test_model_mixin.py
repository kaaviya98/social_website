from django.test import TestCase
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="johnpassword"
        )
