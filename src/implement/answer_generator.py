from openai import OpenAI

def generate_answer(query, similar_questions, faq_data, conversation_history, config):
    client = OpenAI(api_key=config['openai_api_key'])
    
    # 유사도 점수가 0.15 이상인 질문만 사용 (임계값 조정)
    relevant_questions = [q for q in similar_questions if q[1] > 0.15]
    
    if relevant_questions:
        context = "\n".join([f"Q: {q}\nA: {a}" for q, _, a in relevant_questions[:3]])
    else:
        return "죄송합니다. 해당 질문에 대한 정확한 정보를 FAQ에서 찾지 못했습니다. 다른 방식으로 질문을 해주시거나 더 구체적인 정보를 제공해 주시면 도움을 드리겠습니다."
    
    # 최근 3개의 대화만 포함
    recent_conversation = conversation_history[-3:]
    conversation_context = "\n".join([f"Human: {q}\nAI: {a}" for q, a in recent_conversation])
    
    prompt = f"""네이버 스마트스토어 FAQ 도우미입니다. 아래의 사용자 질문에 대해 제공된 FAQ 정보와 대화 기록을 참조하여 답변해 주세요.
    - FAQ 정보를 최우선으로 참조하여 답변하세요. FAQ에 명시된 정보만을 사용하세요.
    - 답변은 FAQ의 내용을 기반으로 하되, 사용자의 질문에 직접적으로 관련된 정보만 간결하게 제공하세요.
    - 불필요한 정보나 맥락에 맞지 않는 내용은 제외하세요.
    - FAQ에 없는 정보는 추측하지 마세요. 확실하지 않은 정보는 제공하지 마세요.
    - 이전 대화 내용을 고려하여 맥락에 맞는 답변을 제공하세요.

    FAQ 정보:
    {context}

    최근 대화:
    {conversation_context}

    사용자 질문: {query}
    답변:"""

    response = client.chat.completions.create(
        model=config['model_name'],
        messages=[
            {"role": "system", "content": "당신은 네이버 스마트스토어에 대한 질문에 답변하는 도우미입니다. FAQ 정보와 대화 기록을 참조하여 정확하고 간결한 답변을 제공하세요."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=config['max_tokens']
    )

    return response.choices[0].message.content.strip()