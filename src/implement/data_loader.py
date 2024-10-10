import pickle

def load_faq_data(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def print_faq_data(faq_data):
    for question, answer in faq_data.items():
        print(f"Q: {question}")
        print(f"A: {answer}")
        print("-" * 50)