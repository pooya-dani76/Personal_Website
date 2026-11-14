from rest_framework import serializers
from .models import SiteInfo
from utils.services import lf
from utils.schemas import LocalizedSerializer, BaseResponseSerializer


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
    
    
class SiteInfoResponseSerializer(BaseResponseSerializer):
    data = SiteInfoSerializer(allow_null=True) 