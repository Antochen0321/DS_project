from api.fastapi import FastAPI
import asyncio
from aiokafka import AIOKafkaProducer

app = FastAPI()
producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")

@app.post("/infer/")
async def infer(prompt: str):
    await producer.start()
    await producer.send("inference_requests", prompt.encode())
    await producer.stop()
    return {"message": "Request sent for inference"}
