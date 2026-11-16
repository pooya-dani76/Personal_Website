from django.db import models
from utils.abstract_models import Publishment, TimeStamped, Orderable
from django_jalali.db import models as jmodels
from skill.models import Skill
from django.utils.text import slugify



class Portfolio(Publishment, TimeStamped):
    slug = models.SlugField(verbose_name="Slug", allow_unicode=True, unique=True, blank=True, editable=False)
    title_en = models.CharField(verbose_name="Title (English)", max_length=100,)
    title_fa = models.CharField(verbose_name="Title (Persian)", max_length=100)
    description_en = models.TextField(verbose_name="Description (English)")
    description_fa = models.TextField(verbose_name="Description (Persian)")
    cover_image = models.ImageField(verbose_name="Cover Image", upload_to='portfolio/covers/', blank=True, null=True)
    technologies = models.ManyToManyField(Skill, blank=True, related_name="projects", verbose_name="Technologies")
    completion_date = jmodels.jDateField(verbose_name="Completion Date")
    live_url = models.URLField(verbose_name="Live URL", blank=True, null=True)
    repo_url = models.URLField(verbose_name="Repository URL", blank=True, null=True)

    def __str__(self):
        return f"{self.title_en} - {self.title_fa}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_en, allow_unicode=True) or slugify(self.title_fa, allow_unicode=True) or "project"
            slug, i = base, 2
            while Portfolio.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
        ordering = ['-created_at']
        db_table = "portfolio"
        
        
        

class PortfolioImage(Publishment, TimeStamped, Orderable):
    project = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(verbose_name="Image", upload_to="portfolio/gallery/")
    caption_fa = models.CharField(verbose_name="Caption (Persian)", max_length=150, blank=True)
    caption_en = models.CharField(verbose_name="Caption (English)", max_length=150, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Portfolio Image"
        verbose_name_plural = "Portfolio Images"
        db_table = "portfolio_image"

    def __str__(self):
        return f"{self.project} #{self.pk}"        