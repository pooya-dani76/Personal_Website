from rest_framework import serializers
from .models import Experience
from utils.services import lf
from utils.schemas import LocalizedSerializer, BaseResponseSerializer


class ExperienceSerializer(LocalizedSerializer):
    
    localized_fields = ("title", "organization", "description")

    class Meta:
        model = Experience
        fields = [
            *lf("title", "organization", "description"),
            "start_date",
            "end_date"
        ]

    
    
class ExperienceResponseSerializer(BaseResponseSerializer):
    data = ExperienceSerializer(many=True) 