from src.implement.vectorizer import get_model

def search_similar_questions(collection, query, top_k=5):
    model = get_model()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["metadatas", "distances", "documents"]
    )
    
    similar_questions = []
    for metadata, distance, document in zip(results['metadatas'][0], results['distances'][0], results['documents'][0]):
        similarity = 1 / (1 + distance)  # Convert distance to similarity score
        similar_questions.append((metadata['question'], similarity, document))
    
    # Sort by similarity score in descending order
    similar_questions.sort(key=lambda x: x[1], reverse=True)
    
    return similar_questions

def is_relevant_question(collection, query, threshold=0.1):
    similar_questions = search_similar_questions(collection, query, top_k=1)
    return len(similar_questions) > 0 and similar_questions[0][1] > threshold