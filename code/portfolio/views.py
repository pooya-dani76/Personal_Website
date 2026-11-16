from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from utils.schemas import BaseErrorResponseSerializer, LANG_PARAM
from utils.services import get_lang, success_message

from .models import Portfolio
from .serializers import PortfolioDetailResponseSerializer, PortfolioListResponseSerializer


class PortfolioListView(APIView):
    @extend_schema(
        summary="List Portfolios",
        description="Returns the published Portfolios",
        parameters=[LANG_PARAM],
        responses={200: PortfolioListResponseSerializer, 403: BaseErrorResponseSerializer},
    )
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        portfolios = Portfolio.objects.filter(is_published=True).prefetch_related("technologies")
        message = success_message("Portfolios", "نمونه‌کارها", lang)
        serializer = PortfolioListResponseSerializer({"message": message, "data": portfolios}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)


class PortfolioDetailView(APIView):
    @extend_schema(
        summary="Retrieve a Portfolio Portfolio",
        description="Returns the full details of one Portfolio (description, gallery & etc).",
        responses={
            200: PortfolioDetailResponseSerializer,
            404: BaseErrorResponseSerializer,
        },
    )
    def get(self, request, slug):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        queryset = Portfolio.objects.filter(is_published=True).prefetch_related("technologies", "images")
        portfolio = get_object_or_404(queryset, slug=slug)
        message = success_message("Portfolio", "نمونه‌کار", lang)
        serializer = PortfolioDetailResponseSerializer({"message": message, "data": portfolio}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)