from typing import Optional, List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import datetime, date

from app.core.config import settings

class OrdersRepository:
    def __init__(self):
        client = MongoClient(settings.mongodb_url)
        db = client[settings.mongodb_db]
        self._coll = db["orders"]
        self._coll.create_index([("order_id", ASCENDING)], unique=True)
        self._coll.create_index([("processing_status", ASCENDING)])

    def insert_many(self, records: List[dict]) -> None:
        if not records:
            return
        try:
            self._coll.insert_many(records, ordered=False)
        except DuplicateKeyError:
            pass

    def find_by_id(self, order_id: str) -> Optional[dict]:
        doc = self._coll.find_one({"order_id": order_id}, {"_id": False})
        if doc is None:
            try:
                iid = int(order_id)
                doc = self._coll.find_one({"order_id": iid}, {"_id": False})
            except ValueError:
                return None

        if not doc:
            return None

        doc["order_id"] = str(doc["order_id"])
        cd = doc.get("calculation_date")
        if isinstance(cd, datetime):
            doc["calculation_date"] = cd.date()
        return doc

    def find_all(self, status: Optional[str], limit: int) -> List[dict]:
        query = {}
        if status:
            query["processing_status"] = status

        raw = self._coll.find(query, {"_id": False}).limit(limit)
        docs: List[dict] = []
        for doc in raw:
            doc["order_id"] = str(doc["order_id"])
            cd = doc.get("calculation_date")
            if isinstance(cd, datetime):
                doc["calculation_date"] = cd.date()
            docs.append(doc)

        return docs
