from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..permissions import Has_role
from ..models import User , Student , Course , Enrollment
from ..serializers.student_serializer import StudentSerializer , RegisterStudentSerailizer
from ..serializers.course_serailzier import CourseSerializer
from ..serializers.enrollment_serialier import EnrollmentSerialzier
from ..serializers.user_serailizer import UserSerializer
from rest_framework.exceptions import PermissionDenied


@api_view(['GET','POST'])
def students(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        students = Student.objects.all()
        return_data = []
        serializer = StudentSerializer(students,many=True)
        for student in serializer.data:
            user = get_object_or_404(User,id=student["user"])
            userSerializer = UserSerializer(user)
            userSerializer.data.pop('id')
            data = {"user_id":user.id,**userSerializer.data,**student}
            return_data.append(data)
        return Response(return_data)
    elif request.method == 'POST':
        serializer = RegisterStudentSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response({
                "id":student.user.id,
                "student_id":student.id,
                "username":student.user.username,
                "email":student.user.email,
                "date_of_birth":student.date_of_birth
        })

@api_view(['PATCH','GET'])
@permission_classes([IsAuthenticated])
def student(request,id):
    student = get_object_or_404(Student,id=id)
    if request.method == 'PATCH':
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        serializer = StudentSerializer(
                student,
                data=request.data,
                partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    elif request.method == 'GET':
        if request.user.role not in [User.Role.STUDENT,User.Role.ADMIN]:
            raise PermissionDenied()
        if request.user.role == User.Role.STUDENT and request.user.student.id != id:
            raise PermissionDenied()
        serializer = StudentSerializer(student)
        courses = student.courses.all()
        courseSerializer = CourseSerializer(courses,many=True)
        return_data = []

        for course in courseSerializer.data:
            enrollment = get_object_or_404(Enrollment,student=id,course=course["id"])
            return_data.append({**course,"progress":enrollment.progress})

        data = {
            **serializer.data,
            "courses":return_data
        }
        return Response(data)    

@api_view(['POST'])
@permission_classes([Has_role(User.Role.STUDENT)])
def enroll(request,course_id):
    course = get_object_or_404(Course,id=course_id)
    std_id = request.user.student.id
    data = {
        "student":std_id,
        "course":course_id
    }

    serialzier = EnrollmentSerialzier(data=data)
    if serialzier.is_valid():
        serialzier.save()
        return Response(serialzier.data)
    return Response(serialzier.errors,status=400)



    

    



    



