from typing import List, Dict
from datetime import datetime
from bson import ObjectId


class ProductsRepository:
    def __init__(self, db_connection):
        self.__collection = db_connection.get_collection("products")

    def insert(self, name: str, sale_price: float, cost: float) -> str:
        doc = {
            "name": name.strip(),
            "sale_price": float(sale_price),
            "cost": float(cost),
            "deleted": False,
            "deleted_at": None,
        }
        res = self.__collection.insert_one(doc)
        return str(res.inserted_id)

    def list_all(self) -> List[Dict]:
        docs = list(
            self.__collection
            .find(
                {"deleted": {"$ne": True}},
                {"name": 1, "sale_price": 1, "cost": 1}
            )
            .sort("name", 1)
        )
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def list_with_pagination(self, page: int, limit: int) -> List[Dict]:
        skip = (page - 1) * limit
        docs = list(
            self.__collection
            .find(
                {"deleted": {"$ne": True}},
                {"name": 1, "sale_price": 1, "cost": 1}
            )
            .sort("name", 1)
            .skip(skip)
            .limit(limit)
        )
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def count_documents(self) -> int:
        return self.__collection.count_documents({"deleted": {"$ne": True}})
    
    def find_by_id(self, product_id: str) -> Dict | None:
        doc = self.__collection.find_one(
            {
                "_id": ObjectId(product_id),
                "deleted": {"$ne": True}
            }
        )

        if not doc:
            return None

        doc["_id"] = str(doc["_id"])
        return doc

    def update(self, product_id: str, update_fields: Dict) -> bool:
        result = self.__collection.update_one(
            {
                "_id": ObjectId(product_id),
                "deleted": {"$ne": True}
            },
            {"$set": update_fields}
        )
        return result.matched_count > 0

    def delete(self, product_id: str) -> bool:
        result = self.__collection.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "deleted": True,
                    "deleted_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    def restore(self, product_id: str) -> bool:
        result = self.__collection.update_one(
            {
                "_id": ObjectId(product_id),
                "deleted": True
            },
            {
                "$set": {
                    "deleted": False,
                    "deleted_at": None
                }
            }
        )
        return result.modified_count > 0

    def list_deleted_with_pagination(self, page: int, limit: int) -> List[Dict]:
        skip = (page - 1) * limit
        docs = list(
            self.__collection
            .find(
                {"deleted": True},
                {"name": 1, "sale_price": 1, "cost": 1, "deleted_at": 1}
            )
            .sort("name", 1)
            .skip(skip)
            .limit(limit)
        )
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def count_deleted_documents(self) -> int:
        return self.__collection.count_documents({"deleted": True})