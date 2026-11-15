from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from .models import Experience
from .serializers import ExperienceResponseSerializer
from utils.services import get_lang, success_message
from drf_spectacular.utils import extend_schema
from utils.schemas import BaseErrorResponseSerializer, LANG_PARAM


class ExperienceView(APIView):
    @extend_schema(
        summary="Retrieve Work Experience Info Data",
        description="This endpoint retrieves work experience data such as title, organization, dates & etc",
        responses={
            200: ExperienceResponseSerializer,
            403: BaseErrorResponseSerializer,
        },
        parameters=[
            LANG_PARAM
        ]
    )
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        message = success_message("Work Experience Info", "اطلاعات سابقه کاری", lang)
        data  = Experience.objects.filter(is_published=True)
        serializer = ExperienceResponseSerializer({"message": message, "data": data}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)