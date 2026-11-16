from django.contrib import admin
from .models import SiteInfo
from utils.services import thumb


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "is_available",
    ]
    ordering = ['-created_at']
    readonly_fields = ("created_at","updated_at", "avatar_thumb",)
    list_editable= ("is_available",)
    
    @admin.display(description="Full Name")
    def full_name(self, obj):
        return f"{obj.name_en} - {obj.name_fa}"
    
    
    @admin.display(description="Avatar Thumbnail")
    def avatar_thumb(self, obj):
        return thumb(obj.avatar, 80)


