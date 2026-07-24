from django.test import TestCase
from app.models import FlashCard , FlashCardReview , FlashCardReviewCourse
from app.ai.utils.global_utils import get_llm
from django.conf import settings
# Create your tests here.
# FlashCard.objects.all().delete()
# FlashCardReview.objects.all().delete()
# FlashCardReviewCourse.objects.all().delete()
# llm = get_llm()
# print(llm.invoke("Hello").content)
print("Hello")
print(settings.MEDIA_ROOT)
