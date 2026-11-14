from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from .models import SiteInfo
from .serializers import SiteInfoResponseSerializer
from utils.services import get_lang, success_message


class SiteInfoView(APIView):
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        message = success_message("Site Info", "اطلاعات سایت", lang)
        serializer = SiteInfoResponseSerializer({"message": message, "data":SiteInfo.load()}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)