import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

import datetime

from ..models import Experience


class ExperienceModelTest(TestCase):
    def test_create_experience(self):
        exp = Experience.objects.create(
            title_fa="توسعه‌دهنده بک‌اند",
            title_en="Backend Developer",
            organization_fa="شرکت Arya",
            organization_en="Arya Company",
            description_fa="توسعه وب سایت",
            description_en="Web development",
            start_date=datetime.date(2022, 1, 1),
            end_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        self.assertEqual(exp.title_fa, "توسعه‌دهنده بک‌اند")
        self.assertEqual(exp.title_en, "Backend Developer")
        self.assertEqual(exp.organization_fa, "شرکت Arya")
        self.assertTrue(exp.is_published)

    def test_experience_str(self):
        exp = Experience.objects.create(
            title_fa="طراح UI",
            title_en="UI Designer",
            start_date=datetime.date(2023, 1, 1),
        )
        self.assertEqual(str(exp), "طراح UI")

    def test_is_current_when_end_date_is_none(self):
        exp = Experience.objects.create(
            title_fa="فعال",
            title_en="Current",
            start_date=datetime.date(2023, 1, 1),
            end_date=None,
            is_published=True,
        )
        self.assertTrue(exp.is_current)

    def test_is_current_when_end_date_is_set(self):
        exp = Experience.objects.create(
            title_fa="پایان یافته",
            title_en="Ended",
            start_date=datetime.date(2022, 1, 1),
            end_date=datetime.date(2023, 1, 1),
            is_published=True,
        )
        self.assertFalse(exp.is_current)

    def test_clean_end_date_before_start_date_raises(self):
        exp = Experience(
            title_fa="تست",
            title_en="Test",
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2022, 1, 1),
            is_published=True,
        )
        with self.assertRaises(ValidationError):
            exp.clean()

    def test_experience_ordering(self):
        exp1 = Experience.objects.create(
            title_fa="قدیم‌تر",
            title_en="Older",
            start_date=datetime.date(2021, 1, 1),
            is_published=True,
        )
        exp2 = Experience.objects.create(
            title_fa="جدید‌تر",
            title_en="Newer",
            start_date=datetime.date(2023, 1, 1),
            is_published=True,
        )
        self.assertEqual(list(Experience.objects.all()), [exp2, exp1])


class ExperienceViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("experience-info")

    def test_get_published_experiences_only(self):
        Experience.objects.create(
            title_fa="منتشر شده",
            title_en="Published",
            start_date=datetime.date(2023, 1, 1),
            is_published=True,
        )
        Experience.objects.create(
            title_fa="پنтовنه",
            title_en="Unpublished",
            start_date=datetime.date(2022, 1, 1),
            is_published=False,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["title"], "منتشر شده")

    def test_get_experiences_with_lang_fa(self):
        Experience.objects.create(
            title_fa="توسعه‌دهنده",
            title_en="Developer",
            start_date=datetime.date(2023, 1, 1),
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "fa"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["title"], "توسعه‌دهنده")

    def test_get_experiences_with_lang_en(self):
        Experience.objects.create(
            title_fa="توسعه‌دهنده",
            title_en="Developer",
            start_date=datetime.date(2023, 1, 1),
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "en"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["title"], "Developer")

    def test_get_experiences_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
