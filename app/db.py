import mysql.connector
from app.config import DB_CONFIG
from app.uuid_service import UuidService
import os
from jinja2 import Template
import json

def run_query_from_file(sql_file, params=None):
    sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'queries', sql_file)
    with open(sql_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    sql = template.render(params or {})
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    products = cursor.fetchall()
    # Преобразуем id из bytes в строку UUID
    for p in products:
        if isinstance(p.get('id'), bytes):
            p['id'] = UuidService.bytes_to_uuid(p['id'])
    cursor.close()
    conn.close()
    return products

def apply_mapping(results, mapping_file):
    mapping_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mappings', mapping_file)
    if not os.path.exists(mapping_path):
        return results
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    mapped = []
    for row in results:
        mapped_row = {api_field: row.get(db_field) for api_field, db_field in mapping.items()}
        mapped.append(mapped_row)
    return mapped