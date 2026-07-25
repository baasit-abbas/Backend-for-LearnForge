from rest_framework import serializers
from ..models import User,Student
from .user_serailizer import UserSerializer
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


    @transaction.atomic
    def create(self,validated_data):
        useSerizlier = UserSerializer(data={
            "username":validated_data["username"],
            "email":validated_data["email"],
            "password":validated_data["password"],
            "role":User.Role.STUDENT
        })
        useSerizlier.is_valid(raise_exception=True)
        user = useSerizlier.save()

        stdSerilzier = StudentSerializer(data={
            "user":user.id,
            "date_of_birth":validated_data["date_of_birth"]
        })

        stdSerilzier.is_valid(raise_exception=True)
        student = stdSerilzier.save()

        return student