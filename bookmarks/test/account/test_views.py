from django.test import TestCase, Client
from .test_model_mixin import ModelMixinTestCase
from django.urls import reverse
from account.forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UserLogin(ModelMixinTestCase, TestCase):
    def test_account_dashboard_GET(self):
        self.client = Client()
        self.assertTrue(self.user.is_active)
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("dashboard"))

        self.assertTemplateUsed(response, "account/dashboard.html")


class UserRegister(ModelMixinTestCase, TestCase):
    def test_user_regiter_returns_registrationform(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.context.get("form"), UserRegistrationForm)

    def test_templates_used_with_register_account(self):

        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(
            response, "account/register.html", "account/register_done.html"
        )

    def test_register_succeeds_registering_users_with_valid_credentials(self):
        self.client.post(
            reverse("register"),
            data={
                "username": "kaaviya",
                "first_name": "Kaaviya",
                "email": "kaaviyaelango98@example.com",
                "password": "kaaviya123",
                "password2": "kaaviya123",
            },
        )
        self.assertTrue(User.objects.filter(username="kaaviya").exists())
