# testimonials/admin.py
from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_en", "rating", "project", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("rating", "is_published")
    search_fields = ("author_fa", "author_en", "quote_fa", "quote_en")
    autocomplete_fields = ("project",)