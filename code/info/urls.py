from django.urls import path
from .views import SiteInfoView



urlpatterns = [
    path('', SiteInfoView.as_view(), name='site-info'),
]
