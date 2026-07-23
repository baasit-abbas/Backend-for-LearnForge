from django.test import TestCase
from app.models import FlashCard , FlashCardReview , FlashCardReviewCourse
from app.ai.utils.global_utils import get_llm
# Create your tests here.
# FlashCard.objects.all().delete()
# FlashCardReview.objects.all().delete()
# FlashCardReviewCourse.objects.all().delete()
llm = get_llm()
print(llm.invoke("Hello").content)