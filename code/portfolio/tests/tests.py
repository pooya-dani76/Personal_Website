from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

import datetime

from skill.models import Skill, SkillCategory
from ..models import Portfolio, PortfolioImage, ProjectFeature


class PortfolioModelTest(TestCase):
    def setUp(self):
        self.skill_cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )
        self.skill = Skill.objects.create(
            name="Django", category=self.skill_cat, is_published=True
        )

    def test_create_portfolio(self):
        portfolio = Portfolio.objects.create(
            title_en="My Portfolio",
            title_fa="نمونه کار من",
            description_en="A portfolio project",
            description_fa="یک پروژه نمونه‌کار",
            completion_date=datetime.date(2024, 1, 15),
            is_published=True,
        )
        portfolio.technologies.add(self.skill)
        self.assertEqual(portfolio.title_en, "My Portfolio")
        self.assertEqual(portfolio.title_fa, "نمونه کار من")
        self.assertTrue(portfolio.is_published)
        self.assertTrue(portfolio.slug)

    def test_portfolio_slug_auto_generation(self):
        portfolio = Portfolio.objects.create(
            title_en="My First Project",
            title_fa="پروژه اول من",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        self.assertEqual(portfolio.slug, "my-first-project")

    def test_portfolio_slug_uniqueness(self):
        Portfolio.objects.create(
            title_en="Same Title",
            title_fa="عنوان一样",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        portfolio2 = Portfolio.objects.create(
            title_en="Same Title",
            title_fa="عنوان一样 ۲",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 2),
            is_published=True,
        )
        self.assertNotEqual(portfolio2.slug, "same-title")
        self.assertTrue(portfolio2.slug.startswith("same-title-"))

    def test_portfolio_str(self):
        portfolio = Portfolio.objects.create(
            title_en="Project A",
            title_fa="پروژه الف",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        self.assertEqual(str(portfolio), "Project A - پروژه الف")

    def test_portfolio_image_str(self):
        portfolio = Portfolio.objects.create(
            title_en="Project",
            title_fa="پروژه",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        image = PortfolioImage.objects.create(
            project=portfolio,
            caption_fa="caption",
            caption_en="Caption",
            order=1,
        )
        self.assertIn(str(image.pk), str(image))
        self.assertIn(portfolio.title_en, str(image.project))

    def test_project_feature_str(self):
        portfolio = Portfolio.objects.create(
            title_en="Project",
            title_fa="پروژه",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        feature = ProjectFeature.objects.create(
            project=portfolio,
            title_fa="ویژگی",
            title_en="Feature",
            order=1,
        )
        self.assertIn("Feature", str(feature))


class PortfolioListViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("portfolio-list")
        self.skill_cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )
        self.skill = Skill.objects.create(
            name="Django", category=self.skill_cat, is_published=True
        )

    def test_get_published_portfolios_only(self):
        Portfolio.objects.create(
            title_en="Published",
            title_fa="منتشر شده",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        Portfolio.objects.create(
            title_en="Unpublished",
            title_fa="منتشر نشده",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 2),
            is_published=False,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["title"], "منتشر شده")

    def test_get_portfolios_with_lang_fa(self):
        Portfolio.objects.create(
            title_en="Project",
            title_fa="پروژه",
            description_en="desc",
            description_fa="توضیحات فارسی",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "fa"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["title"], "پروژه")

    def test_get_portfolios_with_lang_en(self):
        Portfolio.objects.create(
            title_en="Project",
            title_fa="پروژه",
            description_en="Description in English",
            description_fa="توضیحات فارسی",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "en"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["title"], "Project")

    def test_get_portfolios_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PortfolioDetailViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.skill_cat = SkillCategory.objects.create(
            name_fa="توسعه وب", name_en="Web Development"
        )
        self.skill = Skill.objects.create(
            name="Django", category=self.skill_cat, is_published=True
        )
        self.portfolio = Portfolio.objects.create(
            title_en="My Project",
            title_fa="پروژه من",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )
        self.portfolio.technologies.add(self.skill)
        self.url = reverse("portfolio-detail", kwargs={"slug": self.portfolio.slug})

    def test_get_portfolio_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["slug"], self.portfolio.slug)
        self.assertEqual(response.data["data"]["title"], "پروژه من")

    def test_get_portfolio_detail_unpublished_404(self):
        Portfolio.objects.create(
            title_en="Hidden",
            title_fa="پنهان",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=False,
        )
        url = reverse("portfolio-detail", kwargs={"slug": "hidden"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_portfolio_detail_invalid_slug_404(self):
        response = self.client.get(
            reverse("portfolio-detail", kwargs={"slug": "non-existent-slug"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
