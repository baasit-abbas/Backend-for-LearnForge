from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from ..models import Course , User
from ..permissions import Has_role
from ..serializers import CourseSerializer , DocumentSerilizer , VideoSerilizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..ai.utils.global_utils import createOrGetChroma , delete_course , get_embeddings

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
@permission_classes([IsAuthenticated])
def course(request,id):
    course = get_object_or_404(Course,id=id)
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
    if request.method == 'GET':
        if request.user.role == User.Role.STUDENT and id not in request.user.student.courses.values_list("id",flat=True):
            raise PermissionDenied()
        serializer = CourseSerializer(course)
        inst = course.instructor.user.username
        docs = course.docs.all()
        docSerializer = DocumentSerilizer(docs,many=True)
        videos = course.videos.all()
        videoSerialzier = VideoSerilizer(videos,many=True)
        data = {
            **serializer.data,
            "instructor":inst,
            "docs":docSerializer.data,
            "videos":videoSerialzier.data
        }
        return Response(data)
    elif request.method == 'PATCH':
        if request.user.role == User.Role.STUDENT:
            raise PermissionDenied()
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
        if request.user.role == User.Role.STUDENT:
            raise PermissionDenied()
        course.delete()
        embeddings = get_embeddings()
        vector_db = createOrGetChroma(embeddings)
        delete_course(vector_db,str(id))
        return Response({
            "message":"Course deleted",
            "status":200
        })




