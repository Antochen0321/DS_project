from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


from datasets import load_dataset

# Charger un jeu de données jouet
dataset = load_dataset("path/to/your/dataset")

# Préparer les données pour l'entraînement
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")

tokenized_dataset = dataset.map(preprocess_function, batched=True)

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
)

trainer.train()

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/predict/")
def predict(query: Query):
    inputs = tokenizer(query.text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return {"result": tokenizer.decode(outputs[0], skip_special_tokens=True)}

# Lancer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

