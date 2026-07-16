from django.shortcuts import get_list_or_404 , get_object_or_404
from ..models import QuizPerformnace , Course
from ..serializers.quiz_serializer import QuizPerformanceSerailzier
from ..serializers.course_serailzier import CourseSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performace(request):
    user = request.user.id
    all_quizes = get_list_or_404(QuizPerformnace,user=user)
    quizes_serializer = QuizPerformanceSerailzier(all_quizes,many=True)
    return_data = []
    for performace in quizes_serializer.data:
        course = get_object_or_404(Course,id=performace['course'])
        courseserializer = CourseSerializer(course)
        return_data.append({**courseserializer.data,**performace})
    return Response(return_data)