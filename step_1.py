import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# 2. 기본형
@app.get("/")
def main_re():
    return 'hello youngs'

# 3. 루트 접속 시 main 으로 리다이렉트
@app.get("/")
def main_re():
    return RedirectResponse("http://127.0.0.1:8000/main/")

# 4. JSON 값을 리턴하는 API
@app.get("/items/", response_class=JSONResponse)
async def read_items():
    return {"item_id": "Foo"}


# 5-함수 : JSON 값을 리턴하는 API 값 call 함수
async def call_main():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/items/')
        return response.json()

# 5-API : API Call 함수로 값 요청하기
@app.get("/main/")
async def main_page(request: Request):
    client_host = request.client.host
    response_data = await call_main()
    return {"client_host": client_host, "response_data": response_data} #, "response_cal": response_cal}

# 6. get URL
@app.get("/items/line/{item_id}")
async def get_line(item_id: int):
    return item_id

# 7-BaseModel : 값 정리역할
class Item(BaseModel):
    price: int
    cnt: int
    name: str

# 7-response : post test 받은 값을 리턴
@app.post("/items_test/")
async def items_test(item: Item):
    # dict_price = {"item_price": item.price, "item_cnt": item.cnt}
    return item.price * item.cnt, item.name


# 7-requestpost : test json 값과 함께 post 요청
@app.get('/ii/')
async def read_item():
    # POST 요청을 생성하여 /items_test 엔드포인트에 데이터 전송
    async with httpx.AsyncClient() as client:
        item_data = {"price": 10, "cnt": 5, "name":"youngs"}  # 원하는 데이터 설정
        try:
            response = await client.post("http://127.0.0.1:8000/items_test/", json=item_data)
            response.raise_for_status()  # HTTP 오류가 있는 경우 예외 발생
            return {"item_from_post": response.json()}
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}