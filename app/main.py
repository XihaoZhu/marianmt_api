from fastapi import FastAPI
from pydantic import BaseModel
from app.translator import translate

app = FastAPI()



@app.lifespan("startup")
def load_model():
    print("Model loaded")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate_text(request: TranslateRequest):
    result = translate(request.text)
    return {"translation": result}