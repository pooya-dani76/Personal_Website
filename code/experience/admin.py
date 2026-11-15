from django.contrib import admin
from .models import Experience

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "full_info",
        "is_published",
    ]
    ordering = ['-created_at']
    readonly_fields = ("created_at","updated_at")
    list_editable= ("is_published",)
    
    @admin.display(description="Full Info")
    def full_info(self, obj):
        return f"{obj.title_en} in {obj.organization_en}"


