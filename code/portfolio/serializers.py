from rest_framework import serializers
from utils.schemas import BaseResponseSerializer, LocalizedSerializer, BaseSafeImageSerializer
from utils.services import lf
from .models import Portfolio, PortfolioImage, ProjectFeature



class PortfolioImageSerializer(LocalizedSerializer, BaseSafeImageSerializer):
    localized_fields = ("caption",)

    class Meta:
        model = PortfolioImage
        fields = ["image", *lf("caption")]



class ProjectFeatureSerializer(LocalizedSerializer):
    localized_fields = ("title",)

    class Meta:
        model = ProjectFeature
        fields = ["id", *lf("title")]        




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
    localized_fields = ("title", "description")
    images = PortfolioImageSerializer(many=True, read_only=True)
    technologies = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    features = ProjectFeatureSerializer(many=True, read_only=True)

    class Meta(PortfolioListSerializer.Meta):
        fields = [
                    "slug",
                    *lf("title", "description"),
                    "cover_image", "technologies", "completion_date", "live_url",
                    "repo_url", "images", "features",
                ]


class PortfolioListResponseSerializer(BaseResponseSerializer):
    data = PortfolioListSerializer(many=True)


class PortfolioDetailResponseSerializer(BaseResponseSerializer):
    data = PortfolioDetailSerializer()