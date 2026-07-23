from app.ai.prompt.ai_tutor import tutor_prompt
from app.ai.utils.global_utils import *
from django.shortcuts import get_object_or_404
from app.models import FlashCardReviewCourse
import json

def generate_answer(question,course_ids,history=[]):
    vector_db = createOrGetChroma()
    data = get_docs(vector_db,question,course_ids)
    context = data['context']
    print(context)
    llm = get_llm()
    ai_tutor = tutor_prompt | llm
    response = ai_tutor.invoke({
        "question":question,
        "context":context,
        "history":history
    }) 
    return json.loads(response.content)
    
