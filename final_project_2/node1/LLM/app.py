from fastapi import FastAPI
import requests

app = FastAPI()

WORKER_URL = "http://node2_worker:8001"

@app.post("/generate")
def generate_text(prompt: str, max_length: int = 50):
    response = requests.post(f"{WORKER_URL}/generate", json={"prompt": prompt, "max_length": max_length})
    return response.json()

@app.post("/train")
def train_model(data: list[str]):
    response = requests.post(f"{WORKER_URL}/train", json={"data": data})
    return response.json()