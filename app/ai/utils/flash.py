from app.ai.prompt.flashcard import flash_prompt
from app.ai.utils.global_utils import *
import json

def generate_flashcards(context):
    llm = get_llm()
    flash_model = flash_prompt | llm

    res = flash_model.invoke({
        "context":context
    })
    return json.loads(res.content)