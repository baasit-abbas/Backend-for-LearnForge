from django.shortcuts import get_object_or_404 , get_list_or_404
from ..models import FlashCard , FlashCardReview , User , Course
from ..serializers.flashcard_serilaizer import FlashCardSerilizer , FlashCardReviewSerilzier
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..permissions import Has_role
from django.db import transaction

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flashcards(request):
    if request.method == 'GET':
        reviews = get_list_or_404(FlashCardReview,user=request.user.id)
        reviewSerailzier = FlashCardReviewSerilzier(reviews,many=True)
        review_data = []
        for review in reviewSerailzier.data:
            course_name = get_object_or_404(Course,id=review['course']).title
            review_data.append({"course_name":course_name,**review})
        return Response(review_data)

@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.STUDENT)])
def flashcard(request,id):
    course = get_object_or_404(Course,id=id)
    if request.user.role == User.Role.STUDENT and id not in request.user.student.courses.values_list('id',flat=True):
        raise PermissionDenied()
    flashcards = get_list_or_404(FlashCard,course=id)
    serializer = FlashCardSerilizer(flashcards,many=True)
    review = {
        "total":0,
        "attempted":0,
        "marks":0,
        "accuracy":0
    }
    for flashcard in serializer.data:
        flashcardReview = FlashCardReview.objects.filter(user=request.user.id,course=id,flashcard=flashcard['id']).first()
        if flashcardReview:
            review['attempted'] += 1
            review['marks'] += flashcardReview.quality
    review['total'] = review['attempted']*3
    review['accuracy'] = (review['marks'] / review['total']) * 100 if review['total']!=0 else 0

    return Response({
        "flashcards":serializer.data,
        'review':review
    })
    
@api_view(['PATCH'])
@permission_classes([Has_role(User.Role.STUDENT,User.Role.ADMIN)])
def review(request,id):
    flashcard = get_object_or_404(FlashCard,id=id)
    quality_mapping = {
        'Again':FlashCardReview.Quality.AGAIN,
        'Hard':FlashCardReview.Quality.HARD,
        'Good':FlashCardReview.Quality.GOOD,
        'Easy':FlashCardReview.Quality.EASY
    }
    data = {
        "user":request.user.id,
        "course":flashcard.course.id,
        "flashcard":id,
        "quality":quality_mapping[request.data['quality']]
    }
    serilzier = FlashCardReviewSerilzier(data=data)
    serilzier.is_valid(raise_exception=True)
    serilzier.save()

    return Response(serilzier.data)

    








    




