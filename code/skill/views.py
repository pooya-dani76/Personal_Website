from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from .models import Skill, SkillCategory
from .serializers import SkillResponseSerializer, SkillCategoryResponseSerializer
from utils.services import get_lang, success_message
from utils.schemas import BaseErrorResponseSerializer, LANG_PARAM
from drf_spectacular.utils import extend_schema


class SkillView(APIView):
    @extend_schema(
        summary="Get all skills",
        description="Retrieve a list of all published skills.",
        responses={
            200: SkillResponseSerializer,
            403: BaseErrorResponseSerializer,
        },
        parameters=[
            LANG_PARAM
        ]
    )
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        data = Skill.objects.filter(is_published=True)
        message = success_message("Skill Info", "اطلاعات مهارت", lang)
        serializer = SkillResponseSerializer({"message": message, "data": data}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)
    

class SkillCategoryView(APIView):
    @extend_schema(
        summary="Get all skill categories",
        description="Retrieve a list of all skill categories.",
        responses={
            200: SkillCategoryResponseSerializer,
            403: BaseErrorResponseSerializer,
        },
        parameters=[
            LANG_PARAM
        ]
    )
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        data = SkillCategory.objects.all()
        message = success_message("Skill Categories", "دسته بندی مهارت ها", lang)
        serializer = SkillCategoryResponseSerializer({"message": message, "data": data}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)   