from rest_framework import serializers
from ..models import Video , VideoProgress

class VideoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = '__all__'