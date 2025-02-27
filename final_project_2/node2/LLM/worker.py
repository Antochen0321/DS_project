from fastapi import FastAPI
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
import torch

app = FastAPI()

MODEL_PATH = "/Llama-3.2-1B-Instruct"
model = LlamaForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
tokenizer = LlamaTokenizer.from_pretrained(MODEL_PATH)

@app.post("/generate")
def generate_text(prompt: str, max_length: int = 50):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}

@app.post("/train")
def train_model(data: list[str]):
    dataset = [...]
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        logging_dir="./logs",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    trainer.train()
    
    return {"message": "Training completed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)