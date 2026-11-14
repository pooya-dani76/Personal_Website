from django.urls import path
from .views import SkillView, SkillCategoryView



urlpatterns = [
    path('', SkillView.as_view(), name='skill-info'),
    path('categories/', SkillCategoryView.as_view(), name='skill-categories'),
]
