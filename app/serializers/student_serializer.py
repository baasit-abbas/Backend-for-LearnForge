from rest_framework import serializers
from ..models import User,Student
from .user_serailizer import UserSerializer
from django.db import IntegrityError, transaction

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class RegisterStudentSerailizer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    date_of_birth = serializers.DateField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


    @transaction.atomic
    def create(self,validated_data):
        user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
                role=User.Role.STUDENT
            )

        stdSerilzier = StudentSerializer(data={
                "user":user.id,
                "date_of_birth":validated_data["date_of_birth"]
            })

        stdSerilzier.is_valid(raise_exception=True)
        student = stdSerilzier.save()

        return student