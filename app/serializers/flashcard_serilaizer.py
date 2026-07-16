from rest_framework import serializers
from ..models import FlashCard , FlashCardReview

class FlashCardSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = '__all__'

class FlashCardReviewSerilzier(serializers.ModelSerializer):
    class Meta:
        model = FlashCardReview
        fields = '__all__'

        