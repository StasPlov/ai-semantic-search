import os
import re
import logging
from fastapi import FastAPI, Query, Request
from app.db import run_query_from_file, apply_mapping
from app.search_engine import ProductSearchEngine

# Настройка логирования
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

QUERIES_DIR = os.path.join(os.path.dirname(__file__), '..', 'queries')
MAPPINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'mappings')

class ProductSearchEngineDynamic(ProductSearchEngine):
    def __init__(self, products, fields=None):
        self.products = products
        self.fields = fields or []
        product_texts = [
            " ".join(str(p.get(f, "")) for f in self.fields if f != "id" and p.get(f) is not None)
            for p in products
        ]
        super().__init__(products, product_texts)

for fname in os.listdir(QUERIES_DIR):
    if fname.endswith('.sql'):
        route_name = fname.replace('.sql', '')
        mapping_file = f"{route_name}.mapping.json"

        async def endpoint(request: Request, q: str = Query(None)):
            params = {k: v for k, v in request.query_params.items() if k != "q"}
            logger.info(f"Запрос: /query/{route_name} | params={params} | q={q}")
            try:
                results = run_query_from_file(fname, params)
                results = apply_mapping(results, mapping_file)
                if q and results:
                    fields = [f for f in results[0].keys() if f != "id"]
                    if not fields:
                        logger.info(f"/query/{route_name}: нет полей для поиска")
                        return []
                    import time
                    dynamic_engine = ProductSearchEngineDynamic(results, fields=fields)
                    t0 = time.time()
                    search_results = dynamic_engine.search(q)
                    elapsed = (time.time() - t0) * 1000
                    logger.info(f"/query/{route_name}: смысловой поиск занял {elapsed:.2f} мс, найдено {len(search_results)} результатов")
                    return search_results
                logger.info(f"/query/{route_name}: найдено {len(results)} результатов (без смыслового поиска)")
                return results
            except Exception as e:
                logger.exception(f"Ошибка в /query/{route_name}: {e}")
                return {"error": str(e)}

        app.add_api_route(
            f"/query/{route_name}",
            endpoint,
            methods=["GET"],
            name=route_name,
            response_model=list
        ) 
