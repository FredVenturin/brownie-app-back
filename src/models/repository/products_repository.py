from typing import Optional, List, Dict


class ProductsRepository:
    def __init__(self, db_connection):
        self.__collection = db_connection.get_collection("products")

    def insert(self, name: str, sale_price: float, cost: float) -> str:
        doc = {
            "name": name.strip(),
            "sale_price": float(sale_price),
            "cost": float(cost),
        }
        res = self.__collection.insert_one(doc)
        return str(res.inserted_id)

    def list_all(self) -> List[Dict]:
        docs = list(self.__collection.find({}, {"name": 1, "sale_price": 1, "cost": 1}).sort("name", 1))
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs