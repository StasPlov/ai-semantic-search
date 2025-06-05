from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class ProductSearchEngine:
    def __init__(self, products):
        # Сохраняем список товаров
        self.products = products
        # Загружаем предобученную ИИ-модель для преобразования текста в вектор (эмбеддинг)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        # Для каждого товара объединяем название и описание в одну строку
        self.product_texts = [f"{p['title']} {p['description'] or ''}" for p in products]
        # Получаем эмбеддинги как numpy массив (float32)
        self.embeddings = self.model.encode(self.product_texts, convert_to_numpy=True, normalize_embeddings=True)
        if len(self.embeddings) > 0:
            dim = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(self.embeddings)
        else:
            self.index = None

    def search(self, query, top_k=10):
        if self.index is None or len(self.products) == 0:
            return []
        query_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        D, I = self.index.search(query_emb, min(top_k, len(self.products)))
        # I - индексы наиболее похожих товаров
        return [self.products[i] for i in I[0] if i >= 0] 
