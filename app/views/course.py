from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from ..models import Course , User
from ..permissions import Has_role
from ..serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def courses(request):
    if request.method == 'GET':
        if request.user.role not in  [User.Role.ADMIN , User.Role.STUDENT]:
            raise PermissionDenied()
        courses = Course.objects.all()
        serializer = CourseSerializer(courses,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user.role != User.Role.INSTRUCTOR:
            raise PermissionDenied()
        data = {
            **request.data,
            "instructor":request.user.instructor.id
        }
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

@api_view(['GET','PATCH','DELETE'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.INSTRUCTOR)])
def course(request,id):
    course = get_object_or_404(Course,id=id)
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = CourseSerializer(
            course,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    elif request.method == 'DELETE':
        course.delete()
        return Response({
            "message":"Course deleted",
            "status":200
        })


@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.STUDENT)])
def course_of_std(request,course_id,std_id):
    print(request.user.student.id,std_id)
    if request.user.student.id != std_id:
        raise PermissionDenied()
    course = get_object_or_404(
        Course,
        id=course_id,
        students=std_id
    )
    serializer = CourseSerializer(course)
    return Response(serializer.data)



