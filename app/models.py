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
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor")
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
    user = models.OneToOneField(User , on_delete=models.CASCADE,related_name="student")
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    courses = models.ManyToManyField(Course,through="Enrollment",related_name="students")

class Enrollment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)

class Documents(models.Model):
    title = models.CharField(max_length=15)
    fileType = models.CharField(max_length=10)
    fileUrl = models.CharField(max_length=100)

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="docs")
    createdBy = models.ForeignKey(Instructor,on_delete=models.CASCADE,related_name="docs")
    createdAt = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    title = models.CharField(max_length=15)
    thumbnailUrl = models.CharField(max_length=100)
    videoUrl = models.CharField(max_length=100)

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="videos")
    createdBy = models.ForeignKey(Instructor,on_delete=models.CASCADE,related_name="videos")
    createdAt = models.DateTimeField(auto_now_add=True)

class Quiz(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="quizes")
    class Type(models.TextChoices):
        MCQs = 'mcqs',
        TrueFalse = 'true/false'
        Short = 'Short Answers'
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=20,choices=Type.choices)

class MCQ(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="mcqs")
    statment = models.CharField(max_length=255)
    correct = models.CharField(max_length=50)
    selected = models.CharField(default='')

class Options(models.Model):
    mcq = models.ForeignKey(MCQ,on_delete=models.CASCADE,related_name="options")
    statment = models.CharField(max_length=255)

class TrueFalse(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="trueFalse")
    statment = models.CharField(max_length=255)
    correct = models.BooleanField()
    selected = models.CharField(default='')

class ShortAnswers(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="short")
    statment = models.CharField(max_length=255)
    correct = models.CharField(max_length=255)
    selected = models.CharField(default='')

class AiTutor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tutor")
    title = models.CharField(max_length=50)

class ChatMessages(models.Model):
    chat = models.ForeignKey(AiTutor,on_delete=models.CASCADE,related_name="chats")
    class Role(models.TextChoices):
        AI = "ai"
        HUMAN = "human"
    role = models.CharField(max_length=50,choices=Role.choices)
    message = models.CharField(max_length=1000)







    
