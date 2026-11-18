from django.contrib import admin
from .models import Message, ContactInfo


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "seen"
    ]
    list_filter = ['seen']
    ordering = ['-created_at']
    readonly_fields = ("full_name", "email", "message", "seen", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj and not obj.seen:
            obj.seen = True
            obj.save(update_fields=["seen"])
        return obj


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("email",)

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False    