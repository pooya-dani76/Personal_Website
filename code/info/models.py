from django.db import models
from utils.abstract_models import TimeStamped, Publishment


class SiteInfo(TimeStamped):
    """Singleton: the intro/hero data of the site (only one row, pk=1)."""
 
    name_fa = models.CharField(verbose_name="Name (Persian)", max_length=100)
    name_en = models.CharField(verbose_name="Name (English)", max_length=100)
    role_fa = models.CharField(verbose_name="Role (Persian)", max_length=150, blank=True)
    role_en = models.CharField(verbose_name="Role (English)", max_length=150, blank=True)
    headline_fa = models.CharField(verbose_name="Headline (Persian)", max_length=200, blank=True)
    headline_en = models.CharField(verbose_name="Headline (English)", max_length=200, blank=True)
    bio_fa = models.TextField(verbose_name="Bio (Persian)", blank=True)
    bio_en = models.TextField(verbose_name="Bio (English)", blank=True)
    status_fa = models.CharField(verbose_name="Status (Persian)", max_length=120, blank=True)
    status_en = models.CharField(verbose_name="Status (English)", max_length=120, blank=True)
    is_available = models.BooleanField(verbose_name="Available for Collaboration", default=True)
    avatar = models.ImageField(verbose_name="Avatar", upload_to="profile/", blank=True)
    resume_fa = models.FileField(verbose_name="Resume (Persian)", upload_to="resume/", blank=True)
    resume_en = models.FileField(verbose_name="Resume (English)", upload_to="resume/", blank=True)
 
    class Meta:
        verbose_name = "Site Profile"
        verbose_name_plural = "Site Profiles"
        db_table = "site_profile"
 
    def __str__(self):
        return self.name_fa
 
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
 
    def delete(self, *args, **kwargs):  # the singleton cannot be deleted
        return None
 
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
