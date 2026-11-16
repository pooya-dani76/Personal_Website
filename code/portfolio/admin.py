from django.contrib import admin
from .models import Portfolio, PortfolioImage, ProjectFeature
from utils.services import thumb
    

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ("image", "image_preview", "caption_fa", "caption_en", "order", "is_published", "created_at", "updated_at")
    readonly_fields = ("image_preview", "created_at", "updated_at")

    @admin.display(description="Preview")
    def image_preview(self, obj):
        return thumb(obj.image, 80)
    
    
class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ("title_fa", "title_en", "order", "is_published", "created_at", "updated_at")   
    readonly_fields = ("created_at", "updated_at") 


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title_fa", "completion_date", "is_published")
    list_display_links = ("title_fa",)
    list_editable = ("is_published",)
    list_filter = ("is_published",)
    search_fields = ("title_fa", "title_en")
    readonly_fields = ("cover_preview", "slug")
    filter_horizontal = ("technologies",)
    inlines = [PortfolioImageInline, ProjectFeatureInline]
    fieldsets = (
        ("Main Information", {"fields": ("slug", "title_fa", "title_en", "cover_image", "cover_preview")}),
        ("Details", {"fields": ("description_fa", "description_en")}),
        ("Links and Technologies", {"fields": ("technologies", "live_url", "repo_url", "completion_date")}),
        ("Display", {"fields": ("is_published",)}),
    )
    
    @admin.display(description="Cover Thumbnail")
    def cover_thumb(self, obj):
        return thumb(obj.cover_image, 40)

    @admin.display(description="Cover Preview")
    def cover_preview(self, obj):
        return thumb(obj.cover_image, 160)