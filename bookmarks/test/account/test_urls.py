from django.test import TestCase
from django.urls import resolve, reverse
from account.views import dashboard, register
from test.account.test_model_mixin import ModelMixinTestCase


class TestUrls(ModelMixinTestCase, TestCase):
    def test_account_dashboard_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("dashboard")).func,
            dashboard,
        )

    def test_account_register_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("register")).func,
            register,
        )
