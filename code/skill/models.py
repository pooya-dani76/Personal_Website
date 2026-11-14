from django.db import models
from utils.abstract_models import Publishment, TimeStamped


class SkillCategory(TimeStamped):
    slug = models.SlugField(verbose_name="identity", unique=True)
    name_fa = models.CharField(verbose_name="Name(Persian)", max_length=60)
    name_en = models.CharField(verbose_name="Name(English)", max_length=60)

    class Meta:
        db_table = "skill_category"
        ordering = ['-created_at'] 
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name_fa


class Skill(TimeStamped, Publishment):
    name = models.CharField(verbose_name="Name", max_length=60, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name="skills", verbose_name="Category")

    class Meta:
        db_table = "skill"
        ordering = ['-created_at']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name
