from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..permissions import Has_role
from ..models import User , Student
from ..serializers import StudentSerializer , RegisterStudentSerailizer
from rest_framework.exceptions import PermissionDenied


@api_view(['GET','POST'])
def students(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RegisterStudentSerailizer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "id":student.user.id,
                "username":student.user.username,
                "email":student.user.email,
                "date_of_birth":student.date_of_birth,
                "phone":student.phone
            })
        return Response(serializer.errors,status=400)

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
        if request.user.role == User.Role.STUDENT and request.user.id != id:
            raise PermissionDenied()
        serializer = StudentSerializer(student)
        return Response(serializer.data)    

    



    



