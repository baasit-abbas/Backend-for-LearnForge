from rest_framework import serializers
from django.db import IntegrityError, transaction
from ..models import User,Instructor


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

class AddInstructorSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    specialization = serializers.CharField()
    experience_years = serializers.IntegerField()
    phone = serializers.CharField()

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
                role=User.Role.INSTRUCTOR,
            )

        instructor = Instructor.objects.create(
                user=user,
                specialization=validated_data["specialization"],
                experience_years=validated_data["experience_years"],
                phone=validated_data["phone"],
            )

        return instructor
        