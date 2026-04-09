from transformers import MarianMTModel, MarianTokenizer
import torch
import re


MAX_LENGTH = 256

MODEL_NAME = "Helsinki-NLP/opus-mt-en-zh"

tokenizer = None
model = None

def load_model():
    global tokenizer, model
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)

def is_mostly_english(text: str) -> bool:
    letters = re.findall(r"[A-Za-z]", text)
    if not letters:
        return False
    ratio = len(letters) / len(text)
    return ratio > 0.6

def translate(text: str) -> str:

    if tokenizer is None or model is None:
        raise RuntimeError("Model not loaded")

    text = text.strip()

    if not text:
        raise ValueError("Empty text")
    
    if not is_mostly_english(text):
        raise ValueError("Only English text is supported")

    if len(text) > MAX_LENGTH:
        raise ValueError("Text too long")

    """translate text from English to Chinese"""

    encoded = tokenizer(text, return_tensors="pt", padding=True)

    with torch.no_grad():
        translated = model.generate(**encoded)

    return tokenizer.decode(translated[0], skip_special_tokens=True)