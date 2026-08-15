from langchain_core.prompts import ChatPromptTemplate

flash_prompt = ChatPromptTemplate.from_template("""
    You are an expert in generating flashcards you will be provided number and context generate
    best flashcard in English. Return only one dictionary. Just return a dictionary not ```json just dictionary.                                                                                                                                                                                                                                                                                 
                                                
    Context:
    {context}                                           
                                                
    Rules:

    Use ONLY the supplied context.

    Return Disctionary only.

    Format
            {{
                "front_text":"",
                "back_text":""
            }}
""")