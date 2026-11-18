from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

from ..models import Message, ContactInfo


class MessageModelTest(TestCase):
    def test_create_message(self):
        msg = Message.objects.create(
            full_name="علی علوی",
            email="ali@example.com",
            message="سلام، این یک پیام تستی است.",
        )
        self.assertEqual(msg.full_name, "علی علوی")
        self.assertEqual(msg.email, "ali@example.com")
        self.assertFalse(msg.seen)
        self.assertIsNotNone(msg.created_at)

    def test_message_str(self):
        msg = Message.objects.create(
            full_name="مریم محمدی",
            email="maryam@example.com",
            message="تست پیام",
        )
        expected = f"Message from {msg.full_name} <{msg.email}>"
        self.assertEqual(str(msg), expected)

    def test_message_ordering(self):
        msg1 = Message.objects.create(full_name="A", email="a@a.com", message="اول")
        msg2 = Message.objects.create(full_name="B", email="b@b.com", message="دوم")
        self.assertEqual(list(Message.objects.all()), [msg2, msg1])


class ContactInfoModelTest(TestCase):
    def test_singleton_save_sets_pk_1(self):
        info = ContactInfo.objects.create(email="contact@example.com")
        self.assertEqual(info.pk, 1)

    def test_singleton_delete_returns_none(self):
        ContactInfo.objects.create(email="contact@example.com")
        info = ContactInfo.objects.get(pk=1)
        self.assertIsNone(info.delete())
        self.assertTrue(ContactInfo.objects.filter(pk=1).exists())

    def test_load_gets_or_creates(self):
        info = ContactInfo.load()
        self.assertEqual(info.pk, 1)
        info.email = "new@example.com"
        info.save()
        self.assertEqual(ContactInfo.load().email, "new@example.com")

    def test_contact_info_str(self):
        info = ContactInfo.objects.create(email="test@example.com")
        self.assertEqual(str(info), "Contact Information")


class ContactMeViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("message-me")

    def test_create_message_success(self):
        data = {
            "full_name": "نیما راد",
            "email": "nimarad@example.com",
            "message": "این یک پیام تستی است.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Message.objects.filter(email="nimarad@example.com").exists())

    def test_create_message_invalid_email(self):
        data = {
            "full_name": "نیما راد",
            "email": "not-an-email",
            "message": "پیام",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_message_missing_fields(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_message_without_api_key(self):
        self.client.credentials()
        data = {
            "full_name": "نیما راد",
            "email": "nimarad@example.com",
            "message": "پیام",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ContactInfoViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("site-info")

    def test_get_contact_info(self):
        ContactInfo.objects.create(
            email="info@example.com",
            linkedin="https://linkedin.com/in/example",
            github="https://github.com/example",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["email"], "info@example.com")

    def test_get_contact_info_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_contact_info_creates_if_not_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ContactInfo.objects.filter(pk=1).exists())
