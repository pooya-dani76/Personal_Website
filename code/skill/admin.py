from django.contrib import admin
from .models import Skill, SkillCategory



@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_fa", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_published",
    ]
    ordering = ['-created_at']
    readonly_fields = ("created_at","updated_at")
    list_editable= ("is_published",)


