from django.db import models
from django.contrib.auth.models import AbstractUser , User

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        INSTRUCTOR = 'Instructor'
        STUDENT = 'Student'

    role = models.CharField(max_length=10,choices=Role.choices)

class Instructor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)
    experience_years = models.IntegerField()
    phone = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Course(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,related_name="courses")

class Student(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    courses = models.ManyToManyField(Course,through="Enrollment",related_name="students")


class Enrollment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField()
    grade = models.IntegerField()




    
