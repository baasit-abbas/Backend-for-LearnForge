from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..permissions import Has_role
from ..serializers import VideoSerilizer
from ..models import User , Video , Course

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def videos(request):
    if request.method == 'GET':
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        video = Video.objects.all()
        serilzier = VideoSerilizer(video,many=True)
        return Response(serilzier.data)
    elif request.method == 'POST':
        if request.user.role not in [User.Role.ADMIN,User.Role.INSTRUCTOR]:
            raise PermissionDenied()
        course_id = request.data["course"]
        course = get_object_or_404(Course,id=course_id)
        if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
        data = {
            **request.data,
            "createdBy":request.user.instructor.id
        }
        serailzier = VideoSerilizer(data=data)
        if serailzier.is_valid():
            serailzier.save()
            return Response(serailzier.data)
        return Response(serailzier.errors,status=400)

@api_view(['PATCH','DELETE'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.INSTRUCTOR)])
def video(request):
    vid = get_object_or_404(Video,id=id)
    inst_id = vid.createdBy.id
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != inst_id:
        raise PermissionDenied()
    if request.method == 'PATCH':
        if "title" not in request.data and "thumnailUrl" not in request.data:
            return Response({"error":"Only title and thumbnailUrl is updateable","status":400})
        data = {}
        for key,value in request.data.items():
            if key in ["title","thumbnailUrl"]:
                data[key] = value
        serailzer = VideoSerilizer(vid,data=data,partial=True)
        if serailzer.is_valid():
            serailzer.save()
            return Response(serailzer.data)
        return Response(serailzer.errors,status=400)
    elif request.method == 'DELETE':
        vid.delete()
        return Response({"message":"Video Deleted","status":400})

