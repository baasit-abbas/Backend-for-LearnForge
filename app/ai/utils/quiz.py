from app.ai.utils.global_utils import get_llm
from app.ai.prompt.quiz_generation import quiz_prompt
import json

def generate_quiz(question,context):
    llm = get_llm()
    quiz_model = quiz_prompt | llm
    res = quiz_model.invoke({
        "question":question,
        "context":context
    })
    return json.loads(res.content)


