from rest_framework import serializers
from .models import User , Student , Instructor
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def update(self,instance,validated_data):
        password = validated_data.pop("password",None)

        for attr , value  in validated_data.items():
            setattr(instance,attr,value)
        
        if password:
            instance.set_password(password)
        
        instance.save()

        return instance
    


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

    @transaction.atomic
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role = User.Role.INSTRUCTOR
        )

        instructor = Instructor.objects.create(
            user = user,
            specialization = validated_data["specialization"],
            experience_years = validated_data["experience_years"],
            phone = validated_data["phone"]
        )

        return instructor








