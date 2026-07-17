from django.shortcuts import get_list_or_404 , get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import User , Course , Quiz , MCQ , TrueFalse , ShortAnswers , QuizPerformnace
from rest_framework.response import Response
from ..serializers.quiz_serializer import QuizSerailizer , MCQSerailzier , TrueFalseSerailzier , ShortAnswersSerilzier , GenerateQuiz , QuizPerformanceSerailzier
from rest_framework.exceptions import PermissionDenied
from app.ai.utils.global_utils import get_llm

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def quizes(request):
    if request.method == 'GET':
        user_id = request.user.id
        quizes = get_list_or_404(Quiz,user=user_id)
        serializer = QuizSerailizer(quizes,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        question = request.data['question']
        if request.user.role == User.Role.STUDENT:
            courses = request.user.student.courses.values_list('id',flat=True)
        elif request.user.role == User.Role.INSTRUCTOR:
            courses = request.user.instructor.courses.values_list('id',flat=True)
        else:
            courses = Course.objects.values_list('id',flat=True)
        data = {
            'question':question,
            'courses':courses,
            'user_id':request.user.id
        }
        serializer = GenerateQuiz(data=data)
        if serializer.is_valid():
            quiz = serializer.save()
            return Response(quiz)

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def quiz(request,id):
    quiz = get_object_or_404(Quiz,id=id)
    if request.user.id != quiz.user.id:
        raise PermissionDenied()
    if request.method == 'GET':
        res = []
        if quiz.type == Quiz.Type.MCQs:
            mcqs = quiz.mcqs.all()
            for mcq in mcqs:
                data = {}
                data['id'] = mcq.id
                data['mcq'] = mcq.statment
                data['correct'] = mcq.correct
                data['selected'] = mcq.selected
                options = []
                for option in mcq.options.all():
                    options.append({'id':option.id,'statment':option.statment})
                data['options'] = options
                res.append(data)
        elif quiz.type == Quiz.Type.TrueFalse:
            true_false = quiz.trueFalse.all()
            for question in true_false:
                data = {}
                data['id'] = question.id
                data['statment'] = question.statment
                data['correct'] = question.correct
                data['selected'] = question.selected
                res.append(data)
        else:
            short_answrs = quiz.short.all()
            for question in short_answrs:
                data = {}
                data['id'] = question.id
                data['statment'] = question.statment
                data['correct'] = question.correct
                data['selected'] = question.selected
                res.append(data)
        quiz_serilzier = QuizSerailizer(quiz)
        return Response({
            **quiz_serilzier.data,
            "data":res})
    elif request.method == 'PATCH':
        if "title" not in request.data:
            return Response({"error":"Only title is updatable","status":400})
        title = request.data['title']
        serializer = QuizSerailizer(
            quiz,
            data={"title":title},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        quiz.delete()
        return Response({"message":"Quiz Deleted","status":200})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def selected(request,quiz_id,selected_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    course_id = request.data['course_id']
    if request.user.id != quiz.user.id:
        raise PermissionDenied()
    if "selected" not in request.data:
        return Response({'error':'No selected data provided','status':400})
    selected = request.data['selected']
    if quiz.type == Quiz.Type.MCQs:
        mcq = get_object_or_404(MCQ,id=selected_id)
        if mcq.selected:
            return Response({"error":"Cannot select again","status":400})
        total = 0
        if mcq.correct == selected:
            total = 1
        serializer = MCQSerailzier(
            mcq,
            data={"selected":selected},
            partial=True
        )
    elif quiz.type == Quiz.Type.TrueFalse:
        true_false = get_object_or_404(TrueFalse,id=selected_id)
        if true_false.selected:
            return Response({"error":"Cannot select again","status":400})
        total = 0
        if true_false.correct == selected:
            total = 1
        serializer = TrueFalseSerailzier(
            true_false,
            data = {"selected":selected},
            partial=True
        )
    else:
        short = get_object_or_404(ShortAnswers,id=selected_id)
        if short.selected:
            return Response({"error":"Cannot select again","status":400})
        marks = get_llm().invoke(f"You are teacher and the is correct answer of the question {short.correct} and user typed this {selected}. Question is of 1 mark give him marks from 0 to 1 Just return float value")
        total = float(marks.content)
        serializer = ShortAnswersSerilzier(
            short,
            data = {"selected":selected},
            partial=True
        )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    performace = get_object_or_404(QuizPerformnace,user=request.user.id,course=course_id)
    attempted = performace.attempted + 1
    correct = performace.correct + total
    performaceSrialzier = QuizPerformanceSerailzier(
        performace,
        data={
            "attempted":attempted,
            "correct":correct,
            "accuracy":(correct / attempted)*100
        },
        partial=True
    )
    performaceSrialzier.is_valid(raise_exception=True)
    performaceSrialzier.save()

    attempted = quiz.attempted + 1 
    correct = quiz.correct + total

    quiz_serialzier = QuizSerailizer(quiz,
                                data={"attempted":attempted,"correct":correct},
                                partial=True)
    quiz_serialzier.is_valid(raise_exception=True)
    quiz_serialzier.save()

    return Response({"quiz":quiz_serialzier.data,"selected":serializer.data})
        











    


