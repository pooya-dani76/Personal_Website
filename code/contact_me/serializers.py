from rest_framework import serializers
from .models import ContactInfo, Message
from utils.schemas import BaseResponseSerializer


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            "email",
            "linkedin",
            "github",
            "gitlab",
            "instagram",
            "telegram",
            "whatsapp",
        ]
        
        
class ContactInfoResponseSerializer(BaseResponseSerializer):
    data = ContactInfoSerializer()        


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "full_name",
            "email",
            "message",
        ]
        
class MessageResponseSerializer(BaseResponseSerializer):
    data = MessageSerializer()        