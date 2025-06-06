from sentence_transformers import SentenceTransformer
import numpy as np

class ProductSearchEngine:
    def __init__(self, products, product_texts):
        # Сохраняем список товаров
        self.products = products
        # Загружаем предобученную ИИ-модель для преобразования текста в вектор (эмбеддинг)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        # Для каждого товара объединяем название и описание в одну строку
        self.product_texts = product_texts
        # Получаем эмбеддинги как numpy массив (float32)
        self.embeddings = self.model.encode(self.product_texts, convert_to_numpy=True, normalize_embeddings=True)

    def search(self, query, top_k=10):
        if len(self.products) == 0 or len(self.embeddings) == 0:
            return []
        query_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        # Косинусное сходство: просто скалярное произведение, т.к. эмбеддинги уже нормированы
        scores = np.dot(self.embeddings, query_emb)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.products[i] for i in top_indices if scores[i] > 0] 
