from django.shortcuts import get_object_or_404 , get_list_or_404
from ..models import FlashCard , FlashCardReview , User , Course
from ..serializers.flashcard_serilaizer import FlashCardSerilizer , FlashCardReviewSerilzier
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
        flashcard = get_list_or_404(FlashCard,user=request.user.id)
        serializer = FlashCardSerilizer(flashcard,many=True)
        reviews = get_list_or_404(FlashCardReview,user=request.user.id)
        reviewSerailzier = FlashCardReviewSerilzier(reviews,many=True)
        return Response({
            "flashcards":serializer.data,
            "review":reviewSerailzier.data
        })

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
        review = get_object_or_404(FlashCardReview,user=request.user.id,course=id)
        reviewSerializer = FlashCardReviewSerilzier(review)
        return Response({
            "flashcards":serializer.data,
            "review":reviewSerializer.data
        })
    elif request.method == 'POST':
        number = request.data['number']
        review = FlashCardReview.objects.filter(
            user= request.user.id,
            course = id
        )[0]
        accuracy = review.accuracy if review else 0
        flashcards = generate_flashcards(number,accuracy,id)
        all_flashcards = []
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
            all_flashcards.append(serializer.data)
        if review:
            old_total = review.total
            new_total = old_total + number
            reviewSerializer = FlashCardReviewSerilzier(
                review,
                data={"total":new_total},
                partial=True)
            reviewSerializer.is_valid(raise_exception=True)
            reviewSerializer.save()
        else:
            reviewSerializer = FlashCardReviewSerilzier(data={
                "user":request.user.id,
                "course":id,
                "total":number
            })
            reviewSerializer.is_valid(raise_exception=True)
            reviewSerializer.save()
        return Response({
            "flashcards":all_flashcards,
            "review":reviewSerializer.data
        })
    elif request.method == 'PATCH':
        flash_id = request.data['flash_id']
        correct = request.data['correct']
        flash_card = get_object_or_404(FlashCard,id=flash_id)
        if flash_card.correct is not None:
            return Response({"error":"This was already attempted","status":400})
        serializer = FlashCardSerilizer(
            flash_card,
            data={"correct":correct},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        review = get_object_or_404(FlashCardReview,user=request.user.id,course=id)
        attempted = review.attempted + 1
        correct = review.correct + correct

        data = {
            "attempted":attempted,
            "correct":correct,
            "accuracy": (correct / attempted) * 100
        }

        reviewSerializer = FlashCardReviewSerilzier(review,data=data,partial=True)
        reviewSerializer.is_valid(raise_exception=True)
        reviewSerializer.save()
        return Response({
            "flashcards":serializer.data,
            "review":reviewSerializer.data
        })


    




