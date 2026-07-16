from app.ai.prompt.flashcard import flash_prompt
from app.ai.utils.global_utils import *
import random
import json

def generate_flashcards(number,accuracy,course_id):
    vector_db = createOrGetChroma()
    docs = vector_db.get(where={"course_id":course_id})
    total_chunks = len(docs['documents'])
    first = random.randint(0,total_chunks-2)
    seocnd = first+4
    context = ''.join(docs['documents'][first:seocnd])
    llm = get_llm()
    flash_model = flash_prompt | llm

    res = flash_model.invoke({
        "number":number,
        "accuracy":accuracy,
        "context":context
    })
    print(res.content)
    return json.loads(res.content)