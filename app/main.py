from fastapi import FastAPI
from pydantic import BaseModel
from app.translator import translate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

# 定义请求体
class TranslateRequest(BaseModel):
    text: str

# 翻译接口
@app.post("/translate")
def translate_text(request: TranslateRequest):
    result = translate(request.text)
    return {"translation": result}