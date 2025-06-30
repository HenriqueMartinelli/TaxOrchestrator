from typing import Optional, List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import datetime

from app.core.config import settings


# ---------- helpers --------------------------------------------------------- #
def _r2(val: float | int) -> float:
    """Arredonda para 2 casas, mantendo float (para gravar no Mongo)."""
    return round(float(val), 2)


def _fmt2(val: float | int) -> str:
    """Formata número como texto com 2 casas (para devolver na API)."""
    return f"{float(val):.2f}"


def _format_money_out(doc: dict) -> None:
    """Converte todos os campos monetários (pedido + itens) para string 2-casas."""
    for f in ("gross_total", "total_ibs", "total_cbs", "order_total"):
        doc[f] = _fmt2(doc[f])

    for itm in doc["items"]:
        for f in ("unit_price", "value_ibs_item", "value_cbs_item"):
            itm[f] = _fmt2(itm[f])


def _cast_misc_fields(doc: dict) -> None:
    """Ajusta tipos não monetários para resposta da API."""
    doc["order_id"] = str(doc["order_id"])
    cd = doc.get("calculation_date")
    if isinstance(cd, datetime):
        doc["calculation_date"] = cd.date()


# ---------- repository ------------------------------------------------------ #
class OrdersRepository:
    def __init__(self):
        client = MongoClient(settings.mongodb_url)
        db = client[settings.mongodb_db]
        self._coll = db["orders"]
        self._coll.create_index([("order_id", ASCENDING)], unique=True)
        self._coll.create_index([("processing_status", ASCENDING)])

    def insert_many(self, records: List[dict]) -> None:
        """Insere lista de pedidos já calculados; arredonda valores antes de gravar."""
        if not records:
            return

        for rec in records:
            rec["gross_total"] = _r2(rec["gross_total"])
            rec["total_ibs"]   = _r2(rec["total_ibs"])
            rec["total_cbs"]   = _r2(rec["total_cbs"])
            rec["order_total"] = _r2(rec["order_total"])

            for itm in rec["items"]:
                itm["unit_price"]      = _r2(itm["unit_price"])
                itm["value_ibs_item"]  = _r2(itm["value_ibs_item"])
                itm["value_cbs_item"]  = _r2(itm["value_cbs_item"])

        try:
            self._coll.insert_many(records, ordered=False)
        except DuplicateKeyError:
            pass

    def find_by_id(self, order_id: str) -> Optional[dict]:
        doc = self._coll.find_one({"order_id": order_id}, {"_id": False})
        if doc is None and order_id.isdigit():
            doc = self._coll.find_one({"order_id": int(order_id)}, {"_id": False})
        if not doc:
            return None

        _format_money_out(doc)   
        _cast_misc_fields(doc)
        return doc

    def find_all(self, status: Optional[str], limit: int) -> List[dict]:
        query = {"processing_status": status} if status else {}
        cursor = self._coll.find(query, {"_id": False}).limit(limit)

        docs: List[dict] = []
        for doc in cursor:
            _format_money_out(doc)   
            _cast_misc_fields(doc)
            docs.append(doc)
        return docs
