from aiokafka import AIOKafkaConsumer
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B" #just an indicative test, can be switch to any other LLM 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

async def consume():
    consumer = AIOKafkaConsumer("inference_requests", bootstrap_servers="kafka:9092", group_id="ml_workers")
    await consumer.start()
    try:
        async for msg in consumer:
            prompt = msg.value.decode()
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids
            output = model.generate(input_ids, max_length=100)
            response = tokenizer.decode(output[0], skip_special_tokens=True)
            print("Response:", response)
    finally:
        await consumer.stop()

asyncio.run(consume())
