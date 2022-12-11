from django.test import TestCase
from django.urls import resolve, reverse
from account.views import (
    dashboard,
    register,
    edit,
    user_list,
    user_detail,
    user_follow,
)
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

    def test_account_edit_url_is_resolved(self):

        edit_url = reverse("edit")
        self.assertEqual((resolve(edit_url).func), edit)

    def test_account_users_list_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("user_list")).func,
            user_list,
        )

    def test_account_user_detail_url_is_resolved(self):
        self.assertEqual(
            (resolve(reverse("user_detail", args=["john"])).func),
            user_detail,
        )

    def test_account_user_follow_url_is_resolved(self):
        self.assertEqual(
            (resolve(reverse("user_follow")).func),
            user_follow,
        )
