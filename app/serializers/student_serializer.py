from rest_framework import serializers
from ..models import User,Student
from django.db import transaction

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class RegisterStudentSerailizer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    date_of_birth = serializers.DateField()
    phone = serializers.CharField()

    @transaction.atomic
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role = User.Role.STUDENT
        )

        student = Student.objects.create(
            user=user,
            date_of_birth=validated_data["date_of_birth"],
            phone=validated_data["phone"]
        )

        return student