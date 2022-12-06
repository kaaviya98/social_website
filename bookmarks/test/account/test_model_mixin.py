from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="johnpassword"
        )
        Profile.objects.create(user=self.user)
