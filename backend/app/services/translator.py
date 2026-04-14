from deep_translator import GoogleTranslator
from deep_translator import GoogleTranslator

# 1. 고정 선택지 매핑
CUISINE_MAP = {
    "한식": "Korean",
    "양식": "Western",
    "중식": "Chinese",
    "일식": "Japanese",
    "디저트": "Dessert",
    "아무거나": ""
}

def translate_cuisine(korean_cuisine: str) -> str:
    return CUISINE_MAP.get(korean_cuisine, "")

def translate_to_english(korean_text: str) -> str:
    if not korean_text:
        return ""
    # deep-translator 사용
    return GoogleTranslator(source='ko', dest='en').translate(korean_text)

def translate_to_ko(english_text: str) -> str:
    if not english_text:
        return ""
    return GoogleTranslator(source='en', dest='ko').translate(english_text)

def translate_recipe_results(recipes: list) -> list:
    for recipe in recipes:
        if 'title' in recipe:
            recipe['title'] = translate_to_ko(recipe['title'])
    return recipes

def translate_to_ko(text: str):
    if not text or text.strip() == "":
        return "정보 없음"
    
    try:
        # 텍스트가 너무 길면(2000자 이상) 번역이 실패할 수 있으므로 안전하게 처리
        translator = GoogleTranslator(source='en', target='ko')
        
        # 텍스트가 너무 길 경우 문단 단위로 나눠서 번역 (안전장치)
        if len(text) > 2000:
            paragraphs = text.split('.')
            translated_paragraphs = [translator.translate(p) for p in paragraphs if p.strip()]
            return ". ".join(translated_paragraphs)
        
        return translator.translate(text)
    except Exception as e:
        print(f"번역 오류: {e}")
        return text