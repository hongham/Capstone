from app.services.spoonacular import search_recipes_from_api
from app.services.translator import translate_recipe_results, translate_to_english # translate_to_english 추가
from fastapi import HTTPException

EXCHANGE_RATE = 15 

async def get_recipe_recommendations(request_data):
    # 1. 사용자의 한글 입력을 영어로 번역 (핵심!)
    translated_cuisine = translate_to_english(request_data.cuisine)
    translated_ingredients = translate_to_english(request_data.include_ingredients)
    
    # 2. 번역된 키워드로 Spoonacular API 호출
    raw_recipes = await search_recipes_from_api(
        cuisine=translated_cuisine,
        ingredients=translated_ingredients,
        difficulty_tags=request_data.difficulty
    )

    if not raw_recipes:
        raise HTTPException(status_code=404, detail="조건에 맞는 요리를 찾을 수 없습니다.")

    filtered_recipes = []

    # 3. 예산 필터링 (기존 로직 동일)
    for recipe in raw_recipes:
        price_won = recipe.get("pricePerServing", 0) * EXCHANGE_RATE
        if price_won <= request_data.budget:
            filtered_recipes.append(recipe)

    if not filtered_recipes:
        raise HTTPException(status_code=404, detail="금액에 맞는 요리를 찾을 수 없습니다.")

    # 4. 결과물을 다시 한국어로 번역해서 응답
    translated_recipes = translate_recipe_results(filtered_recipes)
    
    final_results = []
    for item in translated_recipes:
        final_results.append({
            "id": item["id"],
            "title": item["title"],
            "image": item["image"],
            "readyInMinutes": item.get("readyInMinutes", 0),
            "estimated_price": int(item.get("pricePerServing", 0) * EXCHANGE_RATE)
        })

    return final_results[:4]