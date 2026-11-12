from rest_framework import serializers
from .models import SiteInfo
from utils.services import lf


class LocalizedSerializer(serializers.ModelSerializer):
    """Collapses `<name>_fa` / `<name>_en` into one `<name>` based on context['lang']."""

    localized_fields = ()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self.context.get("lang", "fa")
        for name in self.localized_fields:
            fa = data.pop(f"{name}_fa", "") or ""
            en = data.pop(f"{name}_en", "") or ""
            data[name] = (en if lang == "en" else fa) or fa or en
        return data


class SiteInfoSerializer(LocalizedSerializer):
    localized_fields = ("name", "role", "headline", "bio", "status")
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteInfo
        fields = [
            "avatar",
            *lf("name", "role", "headline", "bio", "status"),
            "is_available", "resume_url",
        ]

    def get_resume_url(self, obj):
        en = self.context.get("lang") == "en"
        f = (obj.resume_en if en else obj.resume_fa) or obj.resume_fa or obj.resume_en
        if not f:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(f.url) if request else f.url