from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SiteInfo
from .serializers import SiteInfoSerializer
from utils.services import get_lang


class SiteInfoView(APIView):
    def get(self, request):
        ctx = {"request": request, "lang": get_lang(request)}
        return Response(SiteInfoSerializer(SiteInfo.load(), context=ctx).data)