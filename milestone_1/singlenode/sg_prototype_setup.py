from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.utils.data import Dataset, DataLoader

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

class ToyDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        encodings = self.tokenizer(
            item, truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt"
        )
        return encodings.input_ids[0], encodings.attention_mask[0]

data = ["here is an example", "second try", "third try, the most funny one", "no more idea", "...", "last one"]
tokenizer = AutoTokenizer.from_pretrained(model_name)
dataset = ToyDataset(data, tokenizer)
dataloader = DataLoader(dataset, batch_size=2)
