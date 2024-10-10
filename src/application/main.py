import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.implement.data_loader import load_faq_data
from src.implement.vectorizer import create_chroma_collection, insert_questions, get_model
from src.implement.chatbot import run_chatbot

# Configuration
CONFIG = {
    'openai_api_key': "api-key",
    'faq_data_path': os.path.join(project_root, 'src', 'resource', 'final_result.pkl'),
    'model_name': 'gpt-3.5-turbo',
    'max_tokens': 150,
}

def main():
    faq_data = load_faq_data(CONFIG['faq_data_path'])
    questions = list(faq_data.keys())
    
    model = get_model()
    collection = create_chroma_collection()
    insert_questions(collection, questions, faq_data)
    
    run_chatbot(CONFIG, faq_data, collection)

if __name__ == "__main__":
    main()