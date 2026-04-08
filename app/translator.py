from transformers import MarianMTModel, MarianTokenizer
import torch


MAX_LENGTH = 256

MODEL_NAME = "Helsinki-NLP/opus-mt-en-zh"

tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME)

def translate(text: str) -> str:

    if len(text) > MAX_LENGTH:
        return ["Text too long"]

    """translate text from English to Chinese"""

    encoded = tokenizer(text, return_tensors="pt", padding=True)

    with torch.no_grad():
        translated = model.generate(**encoded)

    return tokenizer.decode(translated[0], skip_special_tokens=True)