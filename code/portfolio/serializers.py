from rest_framework import serializers
from utils.schemas import BaseResponseSerializer, LocalizedSerializer, BaseSafeImageSerializer
from utils.services import lf
from .models import Portfolio, PortfolioImage



class PortfolioImageSerializer(LocalizedSerializer, BaseSafeImageSerializer):
    localized_fields = ("caption",)

    class Meta:
        model = PortfolioImage
        fields = ["image", *lf("caption")]


class PortfolioListSerializer(LocalizedSerializer, BaseSafeImageSerializer):
    localized_fields = ("title", "description")
    

    class Meta:
        model = Portfolio
        fields = [
            "slug",
            *lf("title"),
            "cover_image",
        ]


class PortfolioDetailSerializer(PortfolioListSerializer, BaseSafeImageSerializer):
    localized_fields = ("title", "summary", "description", "challenge", "role")
    images = PortfolioImageSerializer(many=True, read_only=True)
    technologies = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta(PortfolioListSerializer.Meta):
        fields = [
                    "slug",
                    *lf("title", "description"),
                    "cover_image", "technologies", "completion_date", "live_url",
                    "repo_url", "images",
                ]


class PortfolioListResponseSerializer(BaseResponseSerializer):
    data = PortfolioListSerializer(many=True)


class PortfolioDetailResponseSerializer(BaseResponseSerializer):
    data = PortfolioDetailSerializer()