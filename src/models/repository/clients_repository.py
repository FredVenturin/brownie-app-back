from typing import Optional, List, Dict
from bson import ObjectId


class ClientsRepository:
    def __init__(self, db_connection):
        self.__collection = db_connection.get_collection("clients")

    def insert(self, name: str, phone: Optional[str] = None) -> str:
        doc = {
            "name": name.strip(),
            "phone": phone.strip() if isinstance(phone, str) and phone.strip() else None,
        }
        res = self.__collection.insert_one(doc)
        return str(res.inserted_id)

    def list_all(self) -> List[Dict]:
        docs = list(self.__collection.find({}, {"name": 1, "phone": 1}).sort("name", 1))
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs