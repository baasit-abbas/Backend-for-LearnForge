from django.test import TestCase
from app.models import FlashCard , FlashCardReview , FlashCardReviewCourse , DocProgress , Enrollment
from app.ai.utils.global_utils import get_llm
from django.conf import settings
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your tests here.
# FlashCard.objects.all().delete()
# FlashCardReview.objects.all().delete()
# FlashCardReviewCourse.objects.all().delete()
# llm = get_llm()
# print(llm.invoke("Hello").content)
# print("Hello")
print(settings.MEDIA_ROOT)

# DocProgress.objects.all().delete()
# Enrollment.objects.all().delete()

# MEDIA_ROOT = os.path.join(BASE_DIR, "upload")
# print(MEDIA_ROOT)

