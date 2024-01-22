import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    price: str
    cnt: str
    @app.post("/items_test/")
    async def items_test(item_price: price, item_cnt: cnt):
        dict_price = dict(price)
        return {item_price, item_cnt}




# 루트 접속 시 main 으로 리다이렉트
@app.get("/")
def main_re():
    return RedirectResponse("http://127.0.0.1:8000/main/")

# JSON 값을 리턴하는 API
@app.get("/items/", response_class=JSONResponse)
async def read_items():
    return {"item_id": "Foo"}

# post 실험을 위한 라우터
# @app.post("/cal_items/")#, response_class=JSONResponse)
# async def cal_items(item_price: price, item_cnt: cnt):
#     return {"item_price": item_price, "item_cnt": item_cnt}#, "total_price": item_price * item_cnt}

# JSON 값을 리턴하는 API 값 call 함수
async def call_main():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/items/')
        return response.json()


# post 실험을 위한 함수
# async def call_cal():
#     async with httpx.AsyncClient() as client:
#         response = await client.post('http://127.0.0.1:8000/cal_items/', json={'item_price': '5', "item_cnt": '6'})
#         return response.json()

# API Call 함수로 값 요청하기
@app.get("/main/")
async def main_page(request: Request):
    client_host = request.client.host
    response_data = await call_main()
    # response_cal = await call_cal()
    return {"client_host": client_host, "response_data": response_data} #, "response_cal": response_cal}

@app.post('/ii/')
async def create_item(item: Item):
    return item