from django.test import TestCase
from app.models import FlashCard , FlashCardReview , FlashCardReviewCourse
# Create your tests here.
# FlashCard.objects.all().delete()
FlashCardReview.objects.all().delete()
FlashCardReviewCourse.objects.all().delete()