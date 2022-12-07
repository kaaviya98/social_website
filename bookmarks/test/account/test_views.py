from django.test import TestCase, Client
from .test_model_mixin import ModelMixinTestCase
from django.urls import reverse


class UserLogin(ModelMixinTestCase, TestCase):
    def test_account_dashboard_GET(self):
        self.client = Client()
        self.assertTrue(self.user.is_active)
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("dashboard"))

        self.assertTemplateUsed(response, "account/dashboard.html")
