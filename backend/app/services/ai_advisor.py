import os
import requests
from dotenv import load_dotenv

def get_ai_advice(ingredient: str, price: str, budget: int = 10000):
    """
    한림대 HAI-GPT(Claude)를 호출하여 예산 기반 맞춤형 조언을 생성합니다.
    """
    load_dotenv()
    api_key = os.getenv("HAI_GPT_API_KEY")
    
    # 한림대 HAI-GPT Anthropic 전용 엔드포인트
    url = "https://factchat-cloud.mindlogic.ai/v1/api/anthropic/messages" 
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # [핵심] AI에게 예산 정보까지 전달하는 프롬프트 수정
    prompt = (
        f"요리 재료 '{ingredient}'의 최저가가 {price}원이야. "
        f"나의 오늘 총 예산은 {budget}원인데, 이 가격이 대학생 입장에서 적당한지, "
        f"전체 예산 대비 비중은 어떤지 고려해서 더 싸게 살 방법이나 대체 재료를 한 문장으로 친절하게 조언해줘."
    )

    # Anthropic(Claude) 전용 데이터 구조
    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 1024,
        "messages": [
            { "role": "user", "content": prompt }
        ]
    }

    try:
        # 응답 지연 방지를 위해 timeout 설정
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Claude 응답 텍스트 추출 (리스트 형태이므로 인덱스 접근)
            return result['content'][0]['text']
        else:
            print(f"❌ AI 서버 응답 에러: {response.status_code}")
            return f"{ingredient} 가격은 {price}원이네요! 예산 내에서 현명하게 소비해 보세요. (AI 서비스 응답 지연)"
            
    except Exception as e:
        print(f"❌ AI 연결 예외 발생: {str(e)}")
        return f"{ingredient} 가격은 {price}원입니다. 예산 {budget}원에 맞춰 구매를 검토해 보세요!"