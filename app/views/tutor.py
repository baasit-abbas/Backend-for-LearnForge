from django.shortcuts import get_object_or_404 , get_list_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import AiTutor , ChatMessages, User , Course
from ..serializers.tutor_serizlizer import AiTutorSerailzier , ChatMessageSerializer
from rest_framework.response import Response
from ..ai.utils.global_utils import *
from ..ai.utils.tutor import generate_answer
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def chats(request):
    if request.method == 'GET':
        all_chats = get_list_or_404(AiTutor,user=request.user.id)
        serilzier = AiTutorSerailzier(all_chats,many=True)
        return Response(serilzier.data)
    elif request.method == 'POST':
        question = request.data['question']
        if request.user.role == User.Role.STUDENT:
            course_ids = request.user.student.courses.values_list('id',flat=True)
        elif request.user.role == User.Role.INSTRUCTOR:
            course_ids = request.user.instructor.courses.values_list('id',flat=True)
        else:
            course_ids = Course.objects.values_list('id',flat=True)
        response = generate_answer(question,course_ids)
        if "title" not in response or "answer" not in response:
            return Response({"error":"Error while giving answer.Try again."})
        return_data = {}
        data = {
            "user":request.user.id,
            "title":response['title']
        }

        ai_srializer = AiTutorSerailzier(data=data)
        ai_srializer.is_valid(raise_exception=True)
        ai_srializer.save()

        return_data.update(ai_srializer.data)

        chat_id = ai_srializer.data['id']
        human_data = {
            "chat":chat_id,
            "role":ChatMessages.Role.HUMAN,
            "message":question
        }

        human_message = ChatMessageSerializer(data=human_data)
        human_message.is_valid(raise_exception=True)
        human_message.save()

        return_data['human'] = human_message.data

        bot_data = {
            "chat":chat_id,
            "role":ChatMessages.Role.AI,
            "message":response["answer"]
        }

        bot_message = ChatMessageSerializer(data=bot_data)
        bot_message.is_valid(raise_exception=True)
        bot_message.save()

        return_data['ai'] = bot_message.data

        return Response(return_data)

@api_view(['GET','POST','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def chat(request,id):
    get_chat = get_object_or_404(AiTutor,id=id)
    if request.user.id != get_chat.user.id:
        raise PermissionDenied()
    if request.method == 'GET':
        serializer = AiTutorSerailzier(get_chat)
        messages = get_chat.chats.all()
        messages_serializer = ChatMessageSerializer(messages,many=True)
        return Response({
            **serializer.data,
            "messages":messages_serializer.data
        })
    elif request.method == 'POST':
        question = request.data['question']
        if request.user.role == User.Role.STUDENT:
            course_ids = request.user.student.courses.values_list('id',flat=True)
        elif request.user.role == User.Role.INSTRUCTOR:
            course_ids = request.user.instructor.courses.values_list('id',flat=True)
        else:
            course_ids = Course.objects.values_list('id',flat=True)
        messages = get_chat.chats.all()
        messages_serializer = ChatMessageSerializer(messages,many=True)
        last_10_chats = messages_serializer.data[-10:]
        response = generate_answer(question,course_ids,last_10_chats)

        chat_id = get_chat.id
        human_data = {
            "chat":chat_id,
            "role":ChatMessages.Role.HUMAN,
            "message":question
        }

        human_message = ChatMessageSerializer(data=human_data)
        human_message.is_valid(raise_exception=True)
        human_message.save()

        bot_data = {
            "chat":chat_id,
            "role":ChatMessages.Role.AI,
            "message":response["answer"]
        }

        bot_message = ChatMessageSerializer(data=bot_data)
        bot_message.is_valid(raise_exception=True)
        bot_message.save()

        return Response({
            "human":human_message.data,
            "ai":bot_message.data
        })
    elif request.method == 'PATCH':
        if 'title' not in request.data:
            return Response({"erorr":"Only title is updatable","status":400})
        title = request.data["title"]
        serializer = AiTutorSerailzier(
            get_chat,
            data={"title":title},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.data == 'DELETE':
        get_chat.delete()
        return Response({"message":"Chat deleted","status":200})





