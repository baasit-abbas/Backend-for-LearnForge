from django.db import models
from django.contrib.auth.models import AbstractUser , User
from datetime import date

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

class Documents(models.Model):
    title = models.CharField(max_length=50)
    fileType = models.CharField(max_length=10)
    fileUrl = models.CharField(max_length=200)

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
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="quizes")
    class Type(models.TextChoices):
        MCQs = 'mcqs',
        TrueFalse = 'true/false'
        Short = 'Short Answers'
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=20,choices=Type.choices)
    total = models.IntegerField()
    attempted = models.IntegerField(default=0)
    correct = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

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
    createdAt = models.DateTimeField(auto_now_add=True)

class ChatMessages(models.Model):
    chat = models.ForeignKey(AiTutor,on_delete=models.CASCADE,related_name="chats")
    class Role(models.TextChoices):
        AI = "ai"
        HUMAN = "human"
    role = models.CharField(max_length=50,choices=Role.choices)
    message = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(auto_now_add=True)


class FlashCard(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="flashcards")

    front_text = models.CharField(max_length=2000)
    back_text = models.CharField(max_length=2000)

    createdAt = models.DateTimeField(auto_now_add=True)

class FlashCardReview(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    flashcard = models.ForeignKey(FlashCard,on_delete=models.CASCADE,related_name="review")
    
    class Quality(models.IntegerChoices):
        AGAIN = 0
        HARD = 1
        GOOD = 2
        EASY = 3

    quality = models.IntegerField(choices=Quality.choices,default=0)
    repitition = models.IntegerField(default=0)
    interval = models.IntegerField(default=1)
    ease_factor = models.FloatField(default=2.5)
    next_review = models.DateField(default=date.today)
    introduced = models.BooleanField(default=False)


class FlashCardReviewCourse(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="review")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="review")

    attempted = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

class QuizPerformnace(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="review_quiz")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="review_quiz")
    
    total = models.IntegerField(default=0)
    attempted = models.IntegerField(default=0)
    correct = models.FloatField(default=0)

    accuracy = models.FloatField(default=0)
    









    
