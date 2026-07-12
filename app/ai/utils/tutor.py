from app.ai.prompt.ai_tutor import tutor_prompt
from app.ai.utils.global_utils import *
import json

def generate_answer(question,context):
    llm = get_llm()
    ai_tutor = tutor_prompt | llm
    response = ai_tutor.invoke({
        "question":question,
        "context":context
    }) 
    return json.loads(response.content)
    
