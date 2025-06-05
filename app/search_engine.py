from sentence_transformers import SentenceTransformer, util

class ProductSearchEngine:
    def __init__(self, products):
        # Сохраняем список товаров
        self.products = products
        # Загружаем предобученную ИИ-модель для преобразования текста в вектор (эмбеддинг)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        # Для каждого товара объединяем название и описание в одну строку
        self.product_texts = [f"{p['title']} {p['description'] or ''}" for p in products]
        # Преобразуем все тексты товаров в векторы (эмбеддинги) — это и есть "понимание смысла" товара
        self.embeddings = self.model.encode(self.product_texts, convert_to_tensor=True)

    def search(self, query, top_k=10):
        # Преобразуем поисковый запрос пользователя в вектор (эмбеддинг)
        query_emb = self.model.encode(query, convert_to_tensor=True)
        # Сравниваем вектор запроса с векторами всех товаров и находим наиболее близкие по смыслу (top_k)
        hits = util.semantic_search(query_emb, self.embeddings, top_k=top_k)[0]
        # Возвращаем товары, которые ближе всего по смыслу к запросу
        return [self.products[hit['corpus_id']] for hit in hits] 