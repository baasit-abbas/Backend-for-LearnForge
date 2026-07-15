from app.ai.utils.global_utils import *
from app.ai.prompt.quiz_generation import quiz_prompt
import json

def generate_quiz(question,course_ids):
    vector_db = createOrGetChroma()
    context = get_docs(vector_db,question,course_ids)
    llm = get_llm()
    quiz_model = quiz_prompt | llm
    res = quiz_model.invoke({
        "question":question,
        "context":context
    })
    return json.loads(res.content)


