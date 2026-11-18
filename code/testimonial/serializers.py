from .models import Testimonial
from utils.schemas import LocalizedSerializer
from utils.services import lf


class TestimonialListSerializer(LocalizedSerializer):

    localized_fields = ("role", "quote", "author")

    class Meta:
        model = Testimonial
        fields = [
            *lf("author", "role", "quote"),
            "avatar",
            "rating",
            "project"
        ]