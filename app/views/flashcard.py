from django.shortcuts import get_object_or_404 , get_list_or_404
from ..models import FlashCard , FlashCardReview , FlashCardReviewCourse , User , Course
from ..serializers.flashcard_serilaizer import FlashCardReviewSerilzier , FlashCardReviewCourseSerilzier , FlashCardSerilizer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from ..permissions import Has_role
from django.db import transaction
from datetime import date , timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flashcards(request):
    reviews = get_list_or_404(FlashCardReviewCourse,user=request.user.id)
    return_data = []
    for review in reviews:
        data = {
            "course_id":review.course.id,
            "course_name":review.course.title,
            "attempted":review.attempted,
            "total":review.total_marks,
            "marks":review.marks,
            "accuracy":review.accuracy
        }
        return_data.append(data)
    
    return Response(return_data)
       
@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN,User.Role.STUDENT)])
@transaction.atomic
def flashcard(request,id):
    course = get_object_or_404(Course,id=id)
    student = request.user
    flashcards = course.flashcards.all()
    FlashCardReviewCourse.objects.get_or_create(
            user=student,
            course=course
        )
    for flashcard in flashcards:
        FlashCardReview.objects.get_or_create(
            user=student,
            flashcard=flashcard,
            course=course
        )
    if request.user.role == User.Role.STUDENT and id not in request.user.student.courses.values_list('id',flat=True):
        raise PermissionDenied()
    
    due_cards = FlashCardReview.objects.filter(user=student,course=course,introduced=True,next_review__lte=date.today())
    new_cards = FlashCardReview.objects.filter(user=student,course=course,introduced=False)[:12]
    all_flashcards = []
    for card in new_cards:
        card.introduced = True
        card.next_review = date.today()
        card.save()
        flashcard = card.flashcard
        serilizer = FlashCardSerilizer(flashcard)
        all_flashcards.append(serilizer.data)
    for card in due_cards:
        flashcard = card.flashcard
        serilizer = FlashCardSerilizer(flashcard)
        all_flashcards.append(serilizer.data)
    review = get_object_or_404(FlashCardReviewCourse,user=student,course=course)
    reviewSerialzier = FlashCardReviewCourseSerilzier(review)
    return Response({
        "flashcards":all_flashcards,
        "review":reviewSerialzier.data
    })
    
@api_view(['PATCH'])
@permission_classes([Has_role(User.Role.STUDENT,User.Role.ADMIN)])
@transaction.atomic
def review(request,id):
    flashcard = get_object_or_404(FlashCard,id=id)
    review = get_object_or_404(FlashCardReview,flashcard=id,user=request.user.id)
    quality_mapping = {
        'Again':FlashCardReview.Quality.AGAIN,
        'Hard':FlashCardReview.Quality.HARD,
        'Good':FlashCardReview.Quality.GOOD,
        'Easy':FlashCardReview.Quality.EASY
    }
    quality = quality_mapping[request.data['quality']]
    if quality <= 1:
        repetition = 0
        interval = 1
        ease_factor = review.ease_factor
    else:
        repetition = review.repitition + 1
        if repetition == 1:
            interval = 1
        elif repetition == 2:
            interval = 6
        else:
            interval = repetition * review.ease_factor
        
        ease_factor = review.ease_factor + (0.1 - (3-quality) * (0.08 + (3-quality) * 0.02))
    next_review = review.next_review + timedelta(days=interval)
    serilaizer = FlashCardReviewSerilzier(
        review,
        data = {
            "repitition":repetition,
            "interval":interval,
            "ease_factor":ease_factor,
            "next_review":next_review
        },
        partial=True
    )
    serilaizer.is_valid(raise_exception=True)
    serilaizer.save()

    review = get_object_or_404(FlashCardReviewCourse,user=request.user,course=flashcard.course)
    attempted = review.attempted + 1
    total_marks = review.total_marks + 3
    marks = review.marks + quality

    reviewSerizlier = FlashCardReviewCourseSerilzier(review,
                                                     data={
                                                    "attempted":attempted,
                                                    "marks":marks,
                                                    "total_marks":total_marks,
                                                    "accuracy": (marks / total_marks)*100
                                                    },
                                                    partial=True)
    reviewSerizlier.is_valid(raise_exception=True)
    reviewSerizlier.save()
    return Response(reviewSerizlier.data)


        


