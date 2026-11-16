from django.db import models
from utils.abstract_models import TimeStamped


class Message(TimeStamped):
    full_name = models.CharField(verbose_name="Full Name", max_length=100)
    email = models.EmailField(verbose_name="Email Address")
    message = models.TextField(verbose_name="Message")
    seen = models.BooleanField(verbose_name="Is Seen", default=False)

    def __str__(self):
        return f"Message from {self.full_name} <{self.email}>"
    
    class Meta:
        db_table = 'Message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']
        
        
class ContactInfo(TimeStamped):
    email = models.EmailField(verbose_name="Email Address")
    linkedin = models.URLField(verbose_name="Linkedin", blank=True, null=True)
    github = models.URLField(verbose_name="GitHub", blank=True, null=True)
    gitlab = models.URLField(verbose_name="GitLab", blank=True, null=True)
    instagram = models.URLField(verbose_name="Instagram", blank=True, null=True)
    telegram = models.URLField(verbose_name="Telegram", blank=True, null=True)
    whatsapp = models.URLField(verbose_name="Whatsapp", blank=True, null=True)

    def __str__(self):
        return "Contact Information"
    
    
    def save(self, *args, **kwargs):
            self.pk = 1
            super().save(*args, **kwargs)
     
     
    def delete(self, *args, **kwargs):  # the singleton cannot be deleted
        return None
    
    
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    
    class Meta:
        db_table = 'ContactInfo'
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'  
        ordering = ['-created_at']      