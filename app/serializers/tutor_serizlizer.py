from rest_framework import serializers
from ..models import AiTutor , ChatMessages


class AiTutorSerailzier(serializers.ModelSerializer):
    class Meta:
        model = AiTutor
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = '__all__'



