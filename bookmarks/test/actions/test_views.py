from django.test import TestCase
from images.models import Image
from actions.models import Action
from django.contrib.auth.models import User
from django.urls import reverse
from actions.utils import create_action


class ActionSteam(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="john", password="johnpassword"
        )
        self.user_2 = User.objects.create_user(
            username="johncena", password="johncenapassword"
        )

        self.image = Image.objects.create(
            user=self.user_2,
            title="tests",
            slug="tests",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )

    def test_action_stream_shows_in_dashboard(self):
        self.client.login(username="john", password="johnpassword")

        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.client.login(username="johncena", password="johncenapassword")
        dashboard_display = self.client.get(reverse("dashboard"))
        self.assertQuerysetEqual(
            dashboard_display.context.get("actions"),
            Action.objects.filter(verb="likes"),
        )

    def test_action_stream_does_not_show_our_own_action_in_dashboard(self):
        self.client.login(username="john", password="johnpassword")

        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        dashboard_display = self.client.get(reverse("dashboard"))
        self.assertQuerysetEqual(dashboard_display.context.get("actions"), [])
