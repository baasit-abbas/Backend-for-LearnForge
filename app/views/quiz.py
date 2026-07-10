from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from ..ai.utils.global_utils import *
from ..ai.utils.quiz import generate_quiz
from ..models import User , Course , Quiz , MCQ , Options
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quizes(request):
    question = request.data['question']
    if request.user.role == User.Role.STUDENT:
        courses = request.user.student.courses.values_list('id',flat=True)
    elif request.user.role == User.Role.INSTRUCTOR:
        courses = request.user.instructor.courses.values_list('id',flat=True)
    else:
        courses = Course.objects.values_list('id',flat=True)
    courses = list(courses)
    embeddings = get_embeddings()
    vector_db = createOrGetChroma(embeddings)
    context = get_docs(vector_db,question,courses)
    res = generate_quiz(question,context)
    if res['type'] == 'mcqs':
        pass
    return Response(res)
    


