from django.db import models
from utils.abstract_models import Publishable, TimeStamped
from django.utils.text import slugify


class SkillCategory(TimeStamped):
    slug = models.SlugField(verbose_name="Slug", unique=True, allow_unicode=True, editable=False)
    name_fa = models.CharField(verbose_name="Name(Persian)", max_length=60)
    name_en = models.CharField(verbose_name="Name(English)", max_length=60)


    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_en, allow_unicode=True) or slugify(self.name_fa, allow_unicode=True) or "skill-category"
            slug, i = base, 2
            while SkillCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return self.name_fa

    class Meta:
        db_table = "skill_category"
        ordering = ['-created_at'] 
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
        


class Skill(TimeStamped, Publishable):
    name = models.CharField(verbose_name="Name", max_length=60, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name="skills", verbose_name="Category")

    class Meta:
        db_table = "skill"
        ordering = ['-created_at']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name
