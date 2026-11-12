from django.contrib import admin
from .models import SiteInfo

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "is_available",
    ]
    ordering = ['-created_at']
    readonly_fields = ("created_at","updated_at")
    list_editable= ("is_available",)
    
    @admin.display(description="Full Name")
    def full_name(self, obj):
        return f"{obj.name_en} - {obj.name_fa}"


