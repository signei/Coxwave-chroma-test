import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_model():
    return model

def create_chroma_collection(collection_name="faq_collection"):
    client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    return client.get_or_create_collection(name=collection_name)

def insert_questions(collection, questions, faq_data):
    embeddings = model.encode(questions).tolist()
    collection.add(
        embeddings=embeddings,
        documents=[faq_data[q] for q in questions],
        ids=[str(i) for i in range(len(questions))],
        metadatas=[{"question": q} for q in questions]
    )