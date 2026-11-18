from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status

import datetime

from portfolio.models import Portfolio
from ..models import Testimonial


class TestimonialModelTest(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(
            title_en="My Project",
            title_fa="پروژه من",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )

    def test_create_testimonial(self):
        testimonial = Testimonial.objects.create(
            quote_fa="خدمت عالی بود",
            quote_en="Great service",
            author_fa="علی علوی",
            author_en="Ala Alavi",
            role_fa="توسعه‌دهنده",
            role_en="Developer",
            rating=5,
            project=self.portfolio,
            is_published=True,
        )
        self.assertEqual(testimonial.quote_fa, "خدمت عالی بود")
        self.assertEqual(testimonial.author_fa, "علی علوی")
        self.assertEqual(testimonial.rating, 5)
        self.assertEqual(testimonial.project, self.portfolio)
        self.assertTrue(testimonial.is_published)

    def test_testimonial_str(self):
        testimonial = Testimonial.objects.create(
            quote_fa="عالی",
            quote_en="Great",
            author_fa="علی",
            author_en="Ala",
            role_fa="توسعه‌دهنده",
            role_en="Developer",
            rating=4,
            is_published=True,
        )
        self.assertIn("Ala", str(testimonial))
        self.assertIn("4", str(testimonial))

    def test_rating_validation_min(self):
        testimonial = Testimonial(
            quote_fa="تست",
            quote_en="Test",
            author_fa="علی",
            author_en="Ala",
            rating=0,
            is_published=True,
        )
        with self.assertRaises(ValidationError):
            testimonial.full_clean()

    def test_rating_validation_max(self):
        testimonial = Testimonial(
            quote_fa="تست",
            quote_en="Test",
            author_fa="علی",
            author_en="Ala",
            rating=6,
            is_published=True,
        )
        with self.assertRaises(ValidationError):
            testimonial.full_clean()

    def test_testimonial_ordering(self):
        t1 = Testimonial.objects.create(
            quote_fa="اول",
            quote_en="First",
            author_fa="A",
            author_en="A",
            order=1,
            is_published=True,
        )
        t2 = Testimonial.objects.create(
            quote_fa="دوم",
            quote_en="Second",
            author_fa="B",
            author_en="B",
            order=2,
            is_published=True,
        )
        self.assertEqual(list(Testimonial.objects.all()), [t1, t2])


class TestimonialListViewTest(APITestCase):
    def setUp(self):
        _, self.api_key = APIKey.objects.create_key(name="test-key")
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        self.url = reverse("testimonial-list")
        self.portfolio = Portfolio.objects.create(
            title_en="My Project",
            title_fa="پروژه من",
            description_en="desc",
            description_fa="توضیحات",
            completion_date=datetime.date(2024, 1, 1),
            is_published=True,
        )

    def test_get_published_testimonials_only(self):
        Testimonial.objects.create(
            quote_fa="منتشر شده",
            quote_en="Published",
            author_fa="ali",
            author_en="ali",
            rating=5,
            project=self.portfolio,
            is_published=True,
        )
        Testimonial.objects.create(
            quote_fa="پنтовنه",
            quote_en="Unpublished",
            author_fa="ali",
            author_en="ali",
            rating=3,
            is_published=False,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["rating"], 5)

    def test_get_testimonials_with_lang_fa(self):
        Testimonial.objects.create(
            quote_fa="نظر فارسی",
            quote_en="Persian quote",
            author_fa="علی",
            author_en="Ala",
            rating=5,
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "fa"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["author"], "علی")

    def test_get_testimonials_with_lang_en(self):
        Testimonial.objects.create(
            quote_fa="نظر فارسی",
            quote_en="Persian quote",
            author_fa="علی",
            author_en="Ala",
            rating=5,
            is_published=True,
        )
        response = self.client.get(self.url, {"lang": "en"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["author"], "Ala")

    def test_get_testimonials_without_api_key(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
