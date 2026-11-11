from django.db import models
from django_jalali.db import models as jmodels
 
 
class TimeStamped(models.Model):
    created_at = jmodels.jDateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = jmodels.jDateTimeField(verbose_name="Updated At", auto_now=True)
 
    class Meta:
        abstract = True
 
 
class Publishment(models.Model):
    is_published = models.BooleanField(verbose_name="Is Published", default=True)
 
    class Meta:
        abstract = True

