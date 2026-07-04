from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from ..models import Documents , User , Course
from ..serializers import DocumentSerilizer
from ..permissions import Has_role

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def docs(request):
    if request.method == 'GET':
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        docs = Documents.objects.all()
        serailzier = DocumentSerilizer(docs,many=True)
        return Response(serailzier.data)
    elif request.method == 'POST':
        if request.user.role not in [User.Role.ADMIN,User.Role.INSTRUCTOR]:
            raise PermissionDenied()
        course_id = request.data["course"]
        course = get_object_or_404(Course,id=course_id)
        if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
        data = {
            **request.data,
            "instructor":course.instructor.id
        }
        serailzier = DocumentSerilizer(data=data)
        if serailzier.is_valid():
            serailzier.save()
            return Response(serailzier.data)
        return Response(serailzier.errors,status=400)

@api_view(['PATCH','DELETE'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.INSTRUCTOR)])
def doc(request,id):
    doc = get_object_or_404(Documents,id=id)
    course = doc.course
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id == course.instrucotr.id:
        raise PermissionDenied()
    if request.method == 'PATCH':
        serialzizer = DocumentSerilizer(
            doc,
            data = request.data["title"],
            partial=True
        )
        if serialzizer.is_valid():
            serialzizer.save()
            return Response(serialzizer.data)
        return Response(serialzizer.errors,status=400)
    elif request.method == 'DELETE':
        doc.delete()
        return Response({
            "message":"Document Deleted",
            "status":200
        })



