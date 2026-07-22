from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from ..models import Documents , User , Course
from ..serializers.document_serailizer import DocumentSerilizer
from ..serializers.flashcard_serilaizer import FlashCardSerilizer
from ..permissions import Has_role
from django.core.files.storage import default_storage
from django.conf import settings
import os
from ..ai.utils.global_utils import *
from app.ai.utils.flash import generate_flashcards
from django.db import transaction

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
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
        file = request.FILES.get("file")
        path = default_storage.save(
            f"upload/docs/{file.name}",
            file
        )
        fileUrl = os.path.join(settings.MEDIA_ROOT,path)
        fileType = file.name.split('.')[1]
        course_id = request.data["course"]
        course = get_object_or_404(Course,id=course_id)
        if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
            raise PermissionDenied()
        data = {
            "title":request.data['title'],
            "fileUrl":fileUrl,
            "fileType":fileType,
            "course":course_id,
            "createdBy":course.instructor.id
        }
        serailzier = DocumentSerilizer(data=data)
        serailzier.is_valid(raise_exception=True)
        serailzier.save()
        docs = read_file(fileUrl)
        chunks = divide_chunks(docs)
        metadata = {
                "course_id":course_id,
                "topic":course.title,
                "chapter":request.data['title']
            }
        vector_db = createOrGetChroma()
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
def doc(request,id):
    doc = get_object_or_404(Documents,id=id)
    inst_id = doc.createdBy.id
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id == inst_id:
        raise PermissionDenied()
    if request.method == 'PATCH':
        if "title" not in request.data:
            return Response({"error":"Only title is updateable","status":400})
        serialzizer = DocumentSerilizer(
            doc,
            data = {"title":request.data["title"]},
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



