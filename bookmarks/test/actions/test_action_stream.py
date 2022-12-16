from django.test import TestCase
from images.models import Image
from django.contrib.auth.models import User
from actions.utils import create_action


class ActionSteam(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="johnpassword"
        )

        self.image = Image.objects.create(
            user=self.user,
            title="tests",
            slug="tests",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )

    def test_create_action_returns_true_for_an_action(self):
        self.client.login(username="john", password="johnpassword")
        self.assertEqual(create_action(self.user, "likes", self.image), True)

    def test_create_action_returns_true_for_different_actions(self):
        self.client.login(username="john", password="johnpassword")

        self.assertEqual(create_action(self.user, "likes", self.image), True)
        self.assertEqual(create_action(self.user, "unlikes", self.image), True)

    def test_create_action_returns_false_for_repeated_same_action_within_a_minute(
        self,
    ):
        self.client.login(username="john", password="johnpassword")

        self.assertEqual(create_action(self.user, "likes", self.image), True)
        self.assertEqual(create_action(self.user, "likes", self.image), False)