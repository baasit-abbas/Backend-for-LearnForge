from langchain_core.prompts import ChatPromptTemplate

flash_prompt = ChatPromptTemplate.from_template("""
    You are an expert in generating flashcards you will be provided number and context generate
    best flashcard according to  difficulty level.                                                                            
    Question:
    Generate {number} flashcards.

    Difficuly:
    {difficulty}                                                                                                                                 
                                                
    Context:
    {context}                                           
                                                
    Rules:

    Use ONLY the supplied context.

    Return JSON only.

    Format

    {{
        "flashcards":[
            {{
                "front_text":"",
                "back_text":""
            }}
        ]
    }}
""")