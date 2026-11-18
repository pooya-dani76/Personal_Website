from django.urls import path
from .views import ContactInfoView, MessageMeView



urlpatterns = [
    path('', ContactInfoView.as_view(), name='site-info'),
    path('message/', MessageMeView.as_view(), name='message-me'),
]
