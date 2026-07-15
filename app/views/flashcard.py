from django.shortcuts import get_object_or_404 , get_list_or_404
from ..models import FlashCard , FlashCardReview , User , Course
from ..serializers.flashcard_serilaizer import FlashCardSerilizer , FlashCardReviewSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from app.ai.utils.flash import generate_flashcards
from django.db import transaction

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flashcards(request):
    if request.method == 'GET':
        flashcards = get_list_or_404(FlashCard,user=request.user.id)
        data = []
        for flashcard in flashcards.all():
            flashSerializer = FlashCardSerilizer(flashcard)
            review = FlashCardReviewSerializer(flashcard.review)
            data.append({
                **flashSerializer.data,
                **review.data
            })
        return Response(data)

@api_view(['GET','POST','PATCH'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def flashcard(request,id):
    course = get_object_or_404(Course,id=id)
    if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != course.instructor.id:
        raise PermissionDenied()
    if request.user.role == User.Role.STUDENT and id not in request.user.student.courses.values_list('id',flat=True):
        raise PermissionDenied()
    if request.method == 'GET':
        flashcards = get_list_or_404(FlashCard,user=request.user.id,course=id)
        serializer = FlashCardSerilizer(flashcards,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        number = request.data['number']
        difficulty = request.data['difficulty']
        flashcards = generate_flashcards(number,difficulty,id)
        return_data = []
        for flashcard in flashcards['flashcards']:
            data = {
                "user":request.user.id,
                "course":id,
                "front_text":flashcard['front_text'],
                "back_text":flashcard['back_text']
            }
            serializer = FlashCardSerilizer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            flash_id = serializer.data['id']

            review = FlashCardReviewSerializer(data={'flashcard':flash_id})
            review.is_valid(raise_exception=True)
            review.save()

            return_data.append({
                **serializer.data,
                "review":review.data
            })
        return Response(return_data)
    elif request.method == 'PATCH':
        flash_id = request.data['flash_id']
        correct = request.data['correct']
        flash_card = get_object_or_404(FlashCard,id=flash_id)
        serializer = FlashCardReviewSerializer(
            flash_card.review,
            data={"correct":correct},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


    




