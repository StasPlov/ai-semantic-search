import uuid
from typing import Any, Union

class UuidService:
    @staticmethod
    def uuid_to_bytes(uuid_str: str) -> bytes:
        """Преобразует строку UUID в 16-байтовое представление (bytes)"""
        return uuid.UUID(uuid_str).bytes

    @staticmethod
    def bytes_to_uuid(b: Union[bytes, bytearray]) -> str:
        """Преобразует 16-байтовое представление (bytes) в строку UUID"""
        return str(uuid.UUID(bytes=b))

    @staticmethod
    def generate_uuid_bytes() -> bytes:
        """Генерирует новый UUID4 и возвращает как 16-байтовое представление"""
        return uuid.uuid4().bytes

    @staticmethod
    def restore_bytes(obj: Any) -> Any:
        """
        Рекурсивно восстанавливает bytes из сериализованных объектов (dict с type=Buffer и data)
        Аналог restoreBuffers из TS
        """
        if isinstance(obj, dict) and obj.get('type') == 'Buffer' and isinstance(obj.get('data'), list):
            return bytes(obj['data'])
        if isinstance(obj, list):
            return [UuidService.restore_bytes(item) for item in obj]
        if isinstance(obj, dict):
            return {k: UuidService.restore_bytes(v) for k, v in obj.items()}
        return obj 