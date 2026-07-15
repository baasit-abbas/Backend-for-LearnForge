from rest_framework import serializers
from ..models import FlashCard

class FlashCardSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = '__all__'

        