from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from app.translator import ensure_model_loaded, translate
import time
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)

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
    ensure_model_loaded()
    yield
    
    print("App shutting down...")

app = FastAPI(lifespan=lifespan)

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/translate")
def translate_text(request: TranslateRequest, req: Request):
    
    ensure_model_loaded()

    ip=req.client.host
    check_rate_limit(ip)
    
    try:
        result = translate(request.text)
        return {"translation": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))