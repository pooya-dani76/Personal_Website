from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from portfolio.models import Portfolio
from utils.abstract_models import Orderable, TimeStamped, Publishable


class Testimonial(Orderable, TimeStamped, Publishable):
    quote_fa = models.TextField(verbose_name="Quote Text(Persian)")
    quote_en = models.TextField(verbose_name="Quote Text (English)")
    author_fa = models.CharField(verbose_name="Author Name (Persian)", max_length=120)
    author_en = models.CharField(verbose_name="Author Name (English)", max_length=120)
    rating = models.PositiveSmallIntegerField(verbose_name="Rating (1 to 5)", default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    project = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials", verbose_name="Project")

    class Meta:
        ordering = ["order"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        db_table = "testimonial"

    def __str__(self):
        return self.author_fa