import os
import re
from fastapi import FastAPI, Query, Request
from app.db import run_query_from_file, apply_mapping
from app.search_engine import ProductSearchEngine

app = FastAPI()

QUERIES_DIR = os.path.join(os.path.dirname(__file__), '..', 'queries')
MAPPINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'mappings')

class ProductSearchEngineDynamic(ProductSearchEngine):
    def __init__(self, products, fields=None):
        self.products = products
        self.fields = fields or []
        # Для всех динамических эндпоинтов используем одну и ту же модель
        self.model = ProductSearchEngine([]).model
        self.product_texts = [
            " ".join(str(p.get(f, "")) for f in self.fields if f != "id" and p.get(f) is not None)
            for p in products
        ]
        self.embeddings = self.model.encode(self.product_texts, convert_to_tensor=True)

for fname in os.listdir(QUERIES_DIR):
    if fname.endswith('.sql'):
        route_name = fname.replace('.sql', '')
        mapping_file = f"{route_name}.mapping.json"

        async def endpoint(request: Request, q: str = Query(None)):
            # Собираем параметры для SQL из query_params, кроме q
            params = {k: v for k, v in request.query_params.items() if k != "q"}
            results = run_query_from_file(fname, params)
            results = apply_mapping(results, mapping_file)
            if q and results:
                fields = [f for f in results[0].keys() if f != "id"]
                if not fields:
                    return []
                dynamic_engine = ProductSearchEngineDynamic(results, fields=fields)
                return dynamic_engine.search(q)
            return results

        app.add_api_route(
            f"/query/{route_name}",
            endpoint,
            methods=["GET"],
            name=route_name,
            response_model=list
        ) 