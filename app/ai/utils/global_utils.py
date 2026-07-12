from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,UnstructuredPowerPointLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI , OpenAIEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

BASE_DIR = Path(__file__).resolve().parents[3]

def read_file(url):
    ext = url.split('.')[1]
    if ext == 'pdf':
        loader = PyPDFLoader(url)
    elif ext == 'docx':
        loader = Docx2txtLoader(url)
    elif ext == 'pptx':
        loader = UnstructuredPowerPointLoader(url)
    elif ext == 'txt':
        loader = TextLoader(url)
    else:
        raise ValueError(f"Unsupported file type {ext}")
    return loader.load()

def divide_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks

def get_llm():
    return ChatOpenAI(model_name="gpt-4o-mini")

def get_embeddings():
    return OpenAIEmbeddings()

def createOrGetChroma(embeddings):
    vector_db = Chroma(
    collection_name="learnforge",
    embedding_function=embeddings,
    persist_directory= str(BASE_DIR)+"/chroma_db"
    )
    return vector_db

def add_docs(vector_db,chunks,course_id):
    for chunk in chunks:
        chunk.metadata = {"course_id":course_id}
    vector_db.add_documents(chunks)

def get_docs(vector_db,question,course_id):
    course_id = list(course_id)
    docs = vector_db.similarity_search(question,k=4,filter={"course_id":{"$in":course_id}})
    context = '\n'.join(doc.page_content for doc in docs)
    return context

def delete_course(vector_db,course_id):
    vector_db.delete(where={course_id:course_id})






