from app.ai.utils.global_utils import *
from app.ai.prompt.quiz_generation import quiz_prompt
import json

def generate_quiz(question,context,accuracy):
    llm = get_llm()
    quiz_model = quiz_prompt | llm
    res = quiz_model.invoke({
        "question":question,
        "context":context,
        "accuracy":accuracy
    })
    return json.loads(res.content)


