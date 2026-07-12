from rest_framework import serializers
from ..models import Enrollment

class EnrollmentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'