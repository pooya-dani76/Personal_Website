from django.urls import path
from .views import PortfolioDetailView, PortfolioListView


urlpatterns = [
    path("", PortfolioListView.as_view(), name="portfolio-list"),
    path("<str:slug>/", PortfolioDetailView.as_view(), name="portfolio-detail"),
]