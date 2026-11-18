from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from utils.schemas import BaseErrorResponseSerializer
from drf_spectacular.utils import extend_schema
from .serializers import ContactInfoResponseSerializer, MessageResponseSerializer, MessageSerializer
from utils.services import get_lang, success_message, success_post_message
from .models import ContactInfo


class MessageMeView(APIView):
    @extend_schema(
        summary="Create a new contact us message",
        description="This endpoint allows users to submit a new contact us message.",
        request = MessageResponseSerializer,
        responses={
            201: MessageResponseSerializer,
            400: BaseErrorResponseSerializer,
            403: BaseErrorResponseSerializer
        },
    )
    def post(self, request: Request):
        lang = get_lang(request)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_serializer = MessageResponseSerializer({
                "message": success_post_message("Message", "پیام", lang),
                "data": serializer.data
            })
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        
        error_serializer = BaseErrorResponseSerializer({"error": serializer.errors})
        return Response(error_serializer.data, status=HTTP_400_BAD_REQUEST)

    
class ContactInfoView(APIView):

    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        message = success_message("Contact Information", "اطلاعات تماس", lang)
        serializer = ContactInfoResponseSerializer({"message": message, "data": ContactInfo.load()}, context=ctx)
        return Response(serializer.data, status=HTTP_200_OK)
            