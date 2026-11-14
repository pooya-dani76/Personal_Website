from rest_framework import serializers
from .models import Skill, SkillCategory
from utils.services import lf
from utils.schemas import LocalizedSerializer, BaseResponseSerializer


class SkillCategorySerializer(LocalizedSerializer):
    
    localized_fields = ("name",)
    
    class Meta:
        model = SkillCategory
        fields = [*lf("name"), "slug"]



class SkillSerializer(serializers.ModelSerializer):

    category_info = SkillCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Skill
        fields = ["name", "category_info"]   
    
    
class SkillResponseSerializer(BaseResponseSerializer):
    data = SkillSerializer(many=True) 
    
class SkillCategoryResponseSerializer(BaseResponseSerializer):
    data = SkillCategorySerializer(many=True)     