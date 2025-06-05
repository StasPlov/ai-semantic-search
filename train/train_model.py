# Скрипт для дообучения sentence-transformers на своих парах "запрос — релевантный товар"
# Пример использования будет позже

from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'pairs.jsonl')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'model_finetuned')

# 1. Загружаем пары из файла
train_samples = []
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Файл с парами для обучения не найден: {DATA_PATH}")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        train_samples.append(InputExample(texts=[item["query"], item["positive"]]))

print(f"Загружено пар для обучения: {len(train_samples)}")

# 2. Загружаем предобученную модель
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 3. DataLoader
train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=8)

# 4. Loss
train_loss = losses.MultipleNegativesRankingLoss(model)

# 5. Дообучение
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=2,
    warmup_steps=10,
    output_path=OUTPUT_PATH
)

print(f"Дообучение завершено! Модель сохранена в {OUTPUT_PATH}")

if __name__ == "__main__":
    print("Тут будет логика дообучения модели!") 
