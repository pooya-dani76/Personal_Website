from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

from ..models import Skill, SkillCategory


class SkillCategoryModelTest(TestCase):
    def test_create_skill_category(self):
        cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )
        self.assertEqual(cat.name_fa, "توسعه وب")
        self.assertEqual(cat.name_en, "Web Development")
        self.assertTrue(cat.slug)

    def test_skill_category_slug_auto_generation(self):
        cat = SkillCategory.objects.create(
            name_fa="دیتابیس", name_en="Database"
        )
        self.assertEqual(cat.slug, "database")

    def test_skill_category_slug_uniqueness(self):
        SkillCategory.objects.create(
            name_fa=" same", name_en="Same"
        )
        cat2 = SkillCategory.objects.create(
            name_fa=" same 2", name_en="Same 2"
        )
        self.assertNotEqual(cat2.slug, "same")
        self.assertTrue(cat2.slug.startswith("same-"))

    def test_skill_category_str(self):
        cat = SkillCategory.objects.create(
            name_fa="فروشگاه", name_en="Shop"
        )
        self.assertEqual(str(cat), "فروشگاه")


class SkillModelTest(TestCase):
    def setUp(self):
        self.cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )

    def test_create_skill(self):
        skill = Skill.objects.create(
            name="Django", category=self.cat, is_published=True
        )
        self.assertEqual(skill.name, "Django")
        self.assertEqual(skill.category, self.cat)
        self.assertTrue(skill.is_published)

    def test_skill_str(self):
        skill = Skill.objects.create(
            name="Python", category=self.cat, is_published=True
        )
        self.assertEqual(str(skill), "Python")

    def test_skill_category_protect_on_delete(self):
        skill = Skill.objects.create(
            name="Django", category=self.cat, is_published=True
        )
        with self.assertRaises(Exception):
            self.cat.delete()


class SkillViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("skill-info")
        self.cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )

    def test_get_published_skills_only(self):
        Skill.objects.create(
            name="Django", category=self.cat, is_published=True
        )
        Skill.objects.create(
            name="Old Framework", category=self.cat, is_published=False
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Django")

    def test_get_skills_with_lang_fa(self):
        Skill.objects.create(
            name="Django", category=self.cat, is_published=True
        )
        response = self.client.get(self.url, {"lang": "fa"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_skills_with_lang_en(self):
        Skill.objects.create(
            name="Django", category=self.cat, is_published=True
        )
        response = self.client.get(self.url, {"lang": "en"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_skills_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SkillCategoryViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("skill-categories")

    def test_get_all_skill_categories(self):
        SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )
        SkillCategory.objects.create(
            name_fa="دیتابیس", name_en="Database"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_skill_categories_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
