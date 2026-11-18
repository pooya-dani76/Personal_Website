from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .serializers import TestimonialListSerializer
from .models import Testimonial
from utils.services import get_lang
from utils.schemas import LANG_PARAM
from .paginations import TestimonialPagination
from utils.schemas import BaseErrorResponseSerializer



class TestimonialListView(APIView):
    @extend_schema(
        summary="List Client Testimonials",
        description="Returns the published client testimonials, each optionally linked to a portfolio project.",
        responses={
            200: TestimonialPagination.get_paginated_response_serializer(serializer=TestimonialListSerializer),
            403: BaseErrorResponseSerializer,
        },
        parameters=[
            LANG_PARAM
        ]
    )
    def get(self, request):
        lang = get_lang(request)
        ctx = {"request": request, "lang": lang}
        paginator = TestimonialPagination()
        testimonials = Testimonial.objects.filter(is_published=True).select_related("project")
        paginated_testimonials = paginator.paginate_queryset(testimonials, request)
        serializer = TestimonialListSerializer(paginated_testimonials, many=True, context=ctx)
        return paginator.get_paginated_response(serializer.data)