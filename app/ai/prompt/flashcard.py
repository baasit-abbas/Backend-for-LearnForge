from langchain_core.prompts import ChatPromptTemplate

flash_prompt = ChatPromptTemplate.from_template("""
    You are an expert in generating flashcards you will be provided number and context generate
    best flashcard according to  difficulty level.                                                                                                                                                                                                                                                                                         
                                                
    Context:
    {context}                                           
                                                
    Rules:

    Use ONLY the supplied context.

    Return JSON only.

    Format
            {{
                "front_text":"",
                "back_text":""
            }}
""")