'''
    RESTFULL API
1. HTTP 요청 : GET, POST, PUT, DELETE 요청
2. CRUD : Create, Read, Update, Delete 기능
3. REST : Server - Client 구조

    예시
1. POST /foods/: 새로운 food 아이템을 생성합니다.
2. GET /foods/: 모든 food 아이템을 조회합니다.
3. GET /foods/{food_id}: 특정 food 아이템을 조회합니다.
4. PUT /foods/{food_id}: 특정 food 아이템을 수정합니다.
5. DELETE /foods/{food_id}: 특정 food 아이템을 삭제합니다.
'''

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse 
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 모델 정의
class FoodItem(BaseModel):
    title: str
    description: str = None

# 음식 목록을 저장할 리스트
foods = []

# 1. food 생성 API
@app.post("/foods/", response_model=FoodItem)
async def create_food(item: FoodItem):
    foods.append(item)
    return item

# 2.food 목록 조회 API
@app.get("/foods/", response_model=List[FoodItem])
async def read_foods():
    return foods

# 3. 특정 food 조회 API
@app.get("/foods/{food_id}", response_model=FoodItem)
async def read_food(food_id: int):
    if 0 <= food_id < len(foods):
        return foods[food_id]
    else:
        raise HTTPException(status_code=404, detail="food not found")

# 4. food 수정 API
@app.put("/foods/{food_id}", response_model=FoodItem)
async def update_food(food_id: int, item: FoodItem):
    if 0 <= food_id < len(foods):
        foods[food_id] = item
        return item
    else:
        raise HTTPException(status_code=404, detail="food not found")

# 5. food 삭제 API
@app.delete("/foods/{food_id}", response_model=FoodItem)
async def delete_food(food_id: int):
    if 0 <= food_id < len(foods):
        deleted_food = foods.pop(food_id)
        return deleted_food
    else:
        raise HTTPException(status_code=404, detail="food not found")

# 6. main page
@app.get("/",response_class=HTMLResponse)
async def main_page(request:Request):
    return templates.TemplateResponse("index.html",context={"request":request})