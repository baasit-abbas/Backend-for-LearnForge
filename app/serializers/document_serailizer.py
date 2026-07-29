from rest_framework import serializers
from ..models import Documents , DocProgress

class DocumentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'

class DocumentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocProgress
        fields = '__all__'
