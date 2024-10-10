from src.implement.answer_generator import generate_answer
from src.implement.similarity import search_similar_questions, is_relevant_question

def run_chatbot(config, faq_data, collection):
    conversation_history = []

    print("챗봇: 안녕하세요! 네이버 스마트스토어에 관해 무엇을 도와드릴까요? (종료하려면 'quit'를 입력하세요)")
    
    while True:
        user_input = input("사용자: ")
        
        if user_input.lower() == 'quit':
            print("챗봇: 대화를 종료합니다. 좋은 하루 되세요!")
            break
        
        if not is_relevant_question(collection, user_input):
            print("챗봇: 죄송합니다. 질문이 네이버 스마트스토어와 관련이 없는 것 같습니다. 스마트스토어에 대한 질문을 부탁드립니다.")
            continue

        try:
            similar_questions = search_similar_questions(collection, user_input)
            answer = generate_answer(user_input, similar_questions, faq_data, conversation_history, config)
            print(f"챗봇: {answer}")
            
            # 대화 기록 업데이트
            conversation_history.append((user_input, answer))
            if len(conversation_history) > 10:  # 최근 10개의 대화만 유지
                conversation_history = conversation_history[-10:]
        except Exception as e:
            print(f"오류가 발생했습니다: {str(e)}")
            print("챗봇: 죄송합니다. 질문을 처리하는 중에 문제가 발생했습니다. 다른 질문을 해주시겠습니까?")