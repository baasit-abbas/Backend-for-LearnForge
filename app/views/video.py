from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..permissions import Has_role
from ..serializers.video_serailzier import VideoSerilizer
from ..serializers.flashcard_serilaizer import *
from ..models import User , Video , Course
from ..ai.utils.global_utils import *
from ..ai.utils.flash import generate_flashcards
from django.core.files.storage import default_storage
from django.conf import settings
import os

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
        video = request.FILES.get('video')
        path = default_storage.save(
            f"upload/video/{video.name}",
            video
        )
        videoUrl = path
        # videoUrl = os.path.join(settings.MEDIA_ROOT,path)
        thumbnail = request.FILES.get('image')
        thumbnailPath = default_storage.save(
            f"upload/images/{thumbnail.name}",
            thumbnail
        )
        thumbnailUrl = thumbnailPath
        # thumbnailUrl = os.path.join(settings.MEDIA_ROOT,thumbnailPath)
        title = request.data['title']
        course_id = request.data["course"]
        course = get_object_or_404(Course,id=course_id)
        if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
        data = {
            "title":title,
            "videoUrl":videoUrl,
            "thumbnailUrl":thumbnailUrl,
            "course":course_id,
            "createdBy":course.instructor.id
        }
        serailzier = VideoSerilizer(data=data)
        serailzier.is_valid(raise_exception=True)
        serailzier.save()
        doc = read_video(videoUrl)
        chunks = divide_chunks([doc])
        vector_db = createOrGetChroma()
        metadata = {
                "topic":course.title,
                "chaper":title,
                "course_id":course_id
        }
        add_docs(vector_db,chunks,metadata)
        for i in range(0,len(chunks),4):
            context = ''.join(chunk.page_content for chunk in chunks[i:i+4])
            flashcard = generate_flashcards(context)
            data = {
                    "course":course_id,
                    "front_text":flashcard['front_text'],
                    "back_text":flashcard['back_text']
                    }
            serializer = FlashCardSerilizer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serailzier.data)

@api_view(['PATCH','DELETE'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.INSTRUCTOR)])
def video(request,id):
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
        if os.path.exists(vid.thumbnailUrl):
            os.remove(vid.thumbnailUrl)
        if os.path.exists(vid.videoUrl):
            os.remove(vid.videoUrl)
        vid.delete()
        return Response({"message":"Video Deleted","status":400})

