from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from app.translator import load_model, translate
import time
from contextlib import asynccontextmanager



request_log = {}

RATE_LIMIT = 30
WINDOW = 60

def check_rate_limit(ip: str):
    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip] if now - t < WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    request_log[ip].append(now)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting... (model should be loaded here)")
    load_model()
    yield
    
    print("App shutting down...")

app = FastAPI(lifespan=lifespan)

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/translate")
def translate_text(request: TranslateRequest, req: Request):
    
    ip=req.client.host

    check_rate_limit(ip)
    
    try:
        result = translate(request.text)
        return {"translation": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))