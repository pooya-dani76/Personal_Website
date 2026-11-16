from django.db import models
from django.core.exceptions import ValidationError
from utils.abstract_models import Publishable, TimeStamped
from django_jalali.db import models as jmodels


class Experience(Publishable, TimeStamped):
    title_fa = models.CharField(verbose_name="Title (Persian)", max_length=150)
    title_en = models.CharField(verbose_name="Title (English)", max_length=150)
    organization_fa = models.CharField(verbose_name="Organization (Persian)", max_length=150, blank=True)
    organization_en = models.CharField(verbose_name="Organization (English)", max_length=150, blank=True)
    description_fa = models.TextField(verbose_name="Description (Persian)", blank=True)
    description_en = models.TextField(verbose_name="Description (English)", blank=True)
    start_date = jmodels.jDateField(verbose_name="Start Date")
    end_date = jmodels.jDateField(verbose_name="End Date", null=True, blank=True, help_text="Empty = Until Today")

    class Meta:
        db_table = "experience" 
        ordering = ["-start_date"]
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"

    def __str__(self):
        return self.title_fa

    @property
    def is_current(self):
        return self.end_date is None

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be before start date."})
