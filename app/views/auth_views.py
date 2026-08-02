from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , APIView , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..permissions import Has_role
from ..models import *
from ..serializers.user_serailizer import UserSerializer
from django.utils import timezone
from django.db.models.functions import ExtractMonth
from django.db.models import Count , Sum

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    return Response({
        "id":request.user.id,
        "username":request.user.username,
        "email":request.user.email,
        "role":request.user.role
        })

@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN)])
def users(request):
    user = User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)

class user(APIView):
    permission_classes = [Has_role(User.Role.ADMIN)]

    def get(self,request,id):
        user = get_object_or_404(User,id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self,request,id):
        user = get_object_or_404(User,id=id)
        serializer = UserSerializer(
            user,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,id):
        user = get_object_or_404(User,id=id)
        user.delete()
        return Response({
            "message":"User deleted","status":200
        })

@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN)])
def admin_data(request):
    total_users = User.objects.all().count()
    recent_users = User.objects.filter(
                        date_joined__year = timezone.now().year,
                        date_joined__month = timezone.now().month
                        ).count()
    averge_users = (recent_users / total_users) * 100 if total_users != 0 else 0
    total_students = Student.objects.all().count()
    recent_students = Student.objects.filter(
                        created_at__year = timezone.now().year,
                        created_at__month = timezone.now().month
                        ).count()
    averge_students = (recent_students / total_students) * 100 if total_students != 0 else 0
    total_instructors = Instructor.objects.all().count()
    recent_instructors = Instructor.objects.filter(
                        created_at__year = timezone.now().year,
                        created_at__month = timezone.now().month
                        ).count()
    averge_instrcutors = (recent_instructors / total_instructors) * 100 if total_instructors != 0 else 0
    total_courses = Course.objects.all().count()
    recent_courses = Course.objects.filter(
                        created_at__year = timezone.now().year,
                        created_at__month = timezone.now().month
                        ).count()
    averge_courses = (recent_courses / total_courses) * 100 if total_courses != 0 else 0
    total_docs = Documents.objects.all().count()
    recent_docs = Documents.objects.filter(
                        created_at__year = timezone.now().year,
                        created_at__month = timezone.now().month
                        ).count()
    averge_docs = (recent_docs / total_docs) * 100 if total_docs != 0 else 0
    total_videos = Video.objects.all().count()
    recent_videos = Video.objects.filter(
                        created_at__year = timezone.now().year,
                        created_at__month = timezone.now().month
                        ).count()
    averge_videos = (recent_videos / total_videos) * 100 if total_videos != 0 else 0
    total_quizes = Quiz.objects.all().count()
    total_flashcards = FlashCard.objects.all().count()
    total_ai_chats = AiTutor.objects.all().count() 
    total_active_users = User.objects.filter(is_active=True).count()
    total_quiz_socre = QuizPerformnace.objects.aggregate(Sum("correct"))['correct__sum']
    total_attempted  = QuizPerformnace.objects.aggregate(Sum("attempted"))['attempted__sum']
    averge_quiz_socre = (total_quiz_socre / total_attempted) * 100
    averge_course_complition = (Enrollment.objects.all().count() / Enrollment.objects.filter(completed=True).count()) * 100

    registeration_per_month = (Student.objects
                              .annotate(month=ExtractMonth("created_at"))
                              .values("month")
                              .annotate(count=Count("id"))
                              .order_by("month"))
    months = {
          1: "Jan",
          2: "Feb",
          3: "Mar",
          4: "Apr",
          5: "May",
          6: "Jun",
          7: "Jul",
          8: "Aug",
          9: "Sep",
          10: "Oct",
          11: "Nov",
          12: "Dec",
    }
    for data in registeration_per_month:
        data['month'] = months[data['month']]
    return Response({
        "total_users":total_users,
        "recent_users":recent_users,
        "average_users":averge_users,
        "total_students":total_students,
        "recent_students":recent_students,
        "average_students":averge_students,
        "total_instructors":total_instructors,
        "recent_instructors":recent_instructors,
        "average_instrctors":averge_instrcutors,
        "total_courses":total_courses,
        "recent_courses":recent_courses,
        "average_courses":averge_courses,
        "total_docs":total_docs,
        "recent_docs":recent_docs,
        "average_docs":averge_docs,
        "total_videos":total_videos,
        "recent_videos":recent_videos,
        "average_videos":averge_videos,
        "total_quizes":total_quizes,
        "total_flashcards":total_flashcards,
        "total_ai_chats":total_ai_chats,
        "total_active_users":total_active_users,
        "averge_quiz_socre":averge_quiz_socre,
        "averge_course_complition":averge_course_complition,
        "registeration_per_month":registeration_per_month
    })
                              


    







