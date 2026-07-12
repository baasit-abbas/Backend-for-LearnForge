from rest_framework import serializers
from ..models import Quiz , MCQ , Options , TrueFalse , ShortAnswers
from django.db import transaction
from ..ai.utils.global_utils import *
from ..ai.utils.quiz import generate_quiz


class QuizSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class MCQSerailzier(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = '__all__'

class OptionsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'

class TrueFalseSerailzier(serializers.ModelSerializer):
    class Meta:
        model = TrueFalse
        fields = '__all__'

class ShortAnswersSerilzier(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswers
        fields = '__all__'

class GenerateQuiz(serializers.Serializer):
    user_id = serializers.IntegerField()
    question = serializers.CharField()
    courses = serializers.ListField()

    @transaction.atomic
    def create(self,validated_data):
        user_id = validated_data['user_id']
        question = validated_data['question']
        courses = validated_data['courses']
        embeddings = get_embeddings()
        vector_db = createOrGetChroma(embeddings)
        context = get_docs(vector_db,question,courses)
        res = generate_quiz(question,context)

        typeMapping = {
            "mcqs":Quiz.Type.MCQs,
            "true/false":Quiz.Type.TrueFalse,
            "Short Answers":Quiz.Type.Short
        }
        data = {
            'user':user_id,
            'title':res['title'],
            'type':typeMapping[res['type']]
            }
        all_mcqs = {}
        quiz = QuizSerailizer(data=data)
        quiz.is_valid(raise_exception=True)
        quiz.save()
        all_mcqs.update(**quiz.data)
        quiz_id = quiz.data['id']
        data = []
        if res['type'] == 'mcqs':
            for mcqs in res['mcqs']:
                one_mcq = {}
                mcqData = {
                    'quiz':quiz_id,
                    'statment':mcqs['statment'],
                    'correct':mcqs['correct']
                }
                mcq = MCQSerailzier(data=mcqData)
                mcq.is_valid(raise_exception=True)
                mcq.save()
                one_mcq.update(**mcq.data)
                options =  []
                mcq_id = mcq.data['id']
                for option in mcqs['options']:
                    optionData = {
                        "mcq":mcq_id,
                        "statment":option
                    }
                    optionSerailizer = OptionsSerailizer(data=optionData)
                    optionSerailizer.is_valid(raise_exception=True)
                    optionSerailizer.save()
                    options.append(optionSerailizer.data)
                one_mcq['options'] = options
                data.append(one_mcq)
                
        elif res['type'] == 'true/false':
            for trueFalse in res['true/false']:
                trueFaleData = {
                    "quiz":quiz_id,
                    "statment":trueFalse['statment'],
                    "correct":trueFalse["correct"]
                }
                trueflaseserializer = TrueFalseSerailzier(data=trueFaleData)
                trueflaseserializer.is_valid(raise_exception=True)
                trueflaseserializer.save()
                data.append(trueflaseserializer.data)
        elif res['type'] == 'Short Answers':
            for short in res['Short Answers']:
                shortData = {
                    "quiz":quiz_id,
                    "statment":short['statment'],
                    "correct":short["correct"]
                }
                shortSerizlizer = ShortAnswersSerilzier(data=shortData)
                shortSerizlizer.is_valid(raise_exception=True)
                shortSerizlizer.save()
                data.append(shortSerizlizer.data)
        else:
            raise ValueError('I can only generate mcqs , true/false and short answers')
        all_mcqs["data"] = data
        return all_mcqs