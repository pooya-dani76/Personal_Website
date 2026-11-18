from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

from ..models import SiteInfo


class SiteInfoModelTest(TestCase):
    def test_create_site_info(self):
        info = SiteInfo.objects.create(
            name_fa="علی علوی",
            name_en="Ali Alavi",
            headline_fa="توسعه‌دهنده بک‌اند",
            headline_en="Backend Developer",
            bio_fa="من یک توسعه‌دهنده هستم",
            bio_en="I am a developer",
            is_available=True,
            years_of_experience=5,
        )
        self.assertEqual(info.name_fa, "علی علوی")
        self.assertEqual(info.name_en, "Ali Alavi")
        self.assertTrue(info.is_available)
        self.assertEqual(info.years_of_experience, 5)

    def test_site_info_str(self):
        info = SiteInfo.objects.create(name_fa="علی", name_en="Ali")
        self.assertEqual(str(info), "علی")

    def test_site_info_education_choices(self):
        info = SiteInfo.objects.create(
            name_fa="علی",
            name_en="Ali",
            education=SiteInfo.Education.MASTER,
        )
        self.assertEqual(info.education, "Master")
        self.assertIn("Master", [c[0] for c in SiteInfo.Education.choices])

    def test_site_info_save_sets_pk_1(self):
        info = SiteInfo.objects.create(name_fa="علی", name_en="Ali")
        self.assertEqual(info.pk, 1)

    def test_site_info_delete_returns_none(self):
        SiteInfo.objects.create(name_fa="علی", name_en="Ali")
        info = SiteInfo.objects.get(pk=1)
        self.assertIsNone(info.delete())
        self.assertTrue(SiteInfo.objects.filter(pk=1).exists())

    def test_site_info_load_gets_or_creates(self):
        info = SiteInfo.load()
        self.assertEqual(info.pk, 1)
        info.name_fa = "مجتبی"
        info.save()
        self.assertEqual(SiteInfo.load().name_fa, "مجتبی")


class SiteInfoViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = "/info/"

    def test_get_site_info(self):
        SiteInfo.objects.create(
            name_fa="علی علوی",
            name_en="Ali Alavi",
            headline_fa="توسعه‌دهنده بک‌اند",
            headline_en="Backend Developer",
            is_available=True,
            years_of_experience=3,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data.get("name"), "علی علوی")
        self.assertEqual(data.get("is_available"), True)

    def test_get_site_info_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_site_info_creates_if_not_exists(self):
        info = SiteInfo.load()
        self.assertEqual(info.pk, 1)
        self.assertTrue(SiteInfo.objects.filter(pk=1).exists())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
