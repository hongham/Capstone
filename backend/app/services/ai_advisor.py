import os
import requests
from dotenv import load_dotenv

def get_ai_advice(ingredient: str, price: str):
    load_dotenv()
    api_key = os.getenv("HAI_GPT_API_KEY")
    
    # 한림대 HAI-GPT Anthropic 전용 엔드포인트
    url = "https://factchat-cloud.mindlogic.ai/v1/api/anthropic/messages" 
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # AI에게 보낼 메시지
    prompt = f"요리 재료 '{ingredient}'의 최저가가 {price}원이야. 대학생 입장에서 이 가격이 적당한지, 더 싸게 살 방법이나 대체 재료를 한 문장으로 친절하게 조언해줘."

    # Anthropic(Claude) 전용 데이터 구조
    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            { "role": "user", "content": prompt }
        ]
    }

    try:
        # 응답 지연을 방지하기 위해 timeout을 30초로 넉넉히 설정
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Claude 응답 텍스트 추출
            return result['content'][0]['text']
        else:
            print(f"❌ AI 서버 응답 에러: {response.status_code}")
            return f"AI 서비스 응답 지연 (코드: {response.status_code})"
            
    except Exception as e:
        print(f"❌ AI 연결 예외 발생: {str(e)}")
        return "AI 서비스를 일시적으로 사용할 수 없습니다."