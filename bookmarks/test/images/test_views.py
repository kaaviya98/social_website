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

    def test_template_used_with_detail_view(self):
        self.client.login(username="john", password="johnpassword")

        Image.objects.create(
            user=self.user,
            title="test-image",
            slug="test-image",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.get(
            reverse("images:detail", args=[1, "test-image"])
        )
        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_image_from_database_exists_in_detail_view(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test-image",
            slug="test-image",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.get(
            reverse("images:detail", args=[1, "test-image"])
        )
        self.assertEqual(response.context.get("image"), self.image)

    def test_detail_view_returns_404_for_no_image(self):
        self.client.login(username="john", password="johnpassword")

        response = self.client.get(
            reverse("images:detail", args=[1, "test-image"])
        )
        self.assertEqual(response.status_code, 404)

    def test_image_like_succeeds_when_called_with_ajax(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test",
            slug="test",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.assertEqual(response.content.decode(), '{"status": "ok"}')

    def test_image_unlike_succeeds_when_called_with_ajax(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="tests",
            slug="tests",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        response = self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "unlike"},
        )

        self.assertEqual(response.content.decode(), '{"status": "ok"}')

    def test_image_like_fails_without_image_id_and_action_when_called_with_ajax(
        self,
    ):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test",
            slug="test",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": "None", "action": "None"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(response.content.decode(), '{"status": "error"}')

    def test_image_like_directly_called_returns_status_code_400(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.post(
            reverse("images:like"),
        )
        self.assertEqual(response.status_code, 400)

    def test_template_used_with_image_list_view(self):
        self.client.login(username="john", password="johnpassword")
        self.create_images(5)
        response = self.client.get(reverse("images:list"))
        self.assertTemplateUsed(
            response, "images/image/list.html", "images/image/list_ajax.html"
        )

    def test_images_list_returns_first_page_as_default(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(
            reverse("images:list"),
            {"images": self.create_images(30)},
        )
        self.assertEqual(response.context.get("images").number, 1)
