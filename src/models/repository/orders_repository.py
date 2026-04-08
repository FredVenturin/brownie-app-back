from bson.objectid import ObjectId
from datetime import datetime
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface


class OrdersRepository(OrdersRepositoryInterface):

    def __init__(self, db_connection) -> None:
        self.__collection_name = "orders"
        self.__db_connection = db_connection


    def insert_document(self, document: dict) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        document["deleted"] = False
        document["deleted_at"] = None
        collection.insert_one(document)


    def insert_list_of_documents(self, list_of_documents: list) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_many(list_of_documents)


    def select_many(self, doc_filter: dict) -> list:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = {"$ne": True}

        return list(collection.find(doc_filter).sort("order_date", -1))

    def select_one(self, doc_filter: dict) -> dict:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = {"$ne": True}

        return collection.find_one(doc_filter)


    def select_many_with_properties(self, doc_filter: dict, projection: dict) -> list:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = {"$ne": True}

        return list(collection.find(doc_filter, projection))
    

    def select_with_pagination(self, doc_filter: dict, page: int, limit: int):
        collection = self.__db_connection.get_collection(self.__collection_name)
        skip = (page - 1) * limit

        doc_filter["deleted"] = {"$ne": True}

        cursor = collection.find(doc_filter).sort("order_date", -1).skip(skip).limit(limit)
        return list(cursor)


    def select_if_property_exists(self, property_name: str) -> dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        return collection.find_one({
            property_name: {"$exists": True},
            "deleted": {"$ne": True}
        })


    def select_by_object_id(self, object_id: str) -> dict:
        collection = self.__db_connection.get_collection(self.__collection_name)

        return collection.find_one({
            "_id": ObjectId(object_id),
            "deleted": {"$ne": True}
        })
    

    def count_documents(self, doc_filter: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = {"$ne": True}

        return collection.count_documents(doc_filter)


    def edit_registry(self, order_id: str, update_fields: dict) -> bool:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_fields}
        )

        return result.modified_count > 0


    def edit_many_registries(self, doc_filter: dict, update_fields: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_many(
            doc_filter,
            {"$set": update_fields}
        )

        return result.modified_count


    def edit_registry_with_increment(self, doc_filter: dict, increment_fields: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_many(
            doc_filter,
            {"$inc": increment_fields}
        )

        return result.modified_count


    def delete_registry(self, order_id: str) -> bool:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "deleted": True,
                    "deleted_at": datetime.utcnow()
                }
            }
        )

        return result.modified_count > 0


    def delete_many_registries(self, doc_filter: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_many(
            doc_filter,
            {
                "$set": {
                    "deleted": True,
                    "deleted_at": datetime.utcnow()
                }
            }
        )

        return result.modified_count
    
    def restore_registry(self, order_id: str) -> bool:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_one(
            {
                "_id": ObjectId(order_id),
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
    
    def select_deleted_with_pagination(self, doc_filter: dict, page: int, limit: int):
        collection = self.__db_connection.get_collection(self.__collection_name)
        skip = (page - 1) * limit

        doc_filter["deleted"] = True

        cursor = collection.find(doc_filter).sort("order_date", -1).skip(skip).limit(limit)
        return list(cursor)
    
    def count_deleted_documents(self, doc_filter: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = True

        return collection.count_documents(doc_filter)
    

    def count_by_status(self) -> dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        pipeline = [
            {"$match": {"deleted": {"$ne": True}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        ]
        result = list(collection.aggregate(pipeline))
        stats = {
            "total": 0,
            "confirmed": 0,
            "preparing": 0,
            "packed": 0,
            "sold": 0,
            "cancelled": 0,
        }
        for item in result:
            status = item.get("_id") or ""
            count = item.get("count", 0)
            stats["total"] += count
            if status in stats:
                stats[status] = count
        return stats


    def aggregate_profit_summary(
        self,
        daily_start, daily_end,
        monthly_start, monthly_end,
        annual_start, annual_end,
    ) -> dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        pipeline = [
            {
                "$match": {
                    "status": "sold",
                    "deleted": {"$ne": True},
                    "itens": {"$exists": True, "$ne": []},
                }
            },
            {"$unwind": "$itens"},
            {
                "$addFields": {
                    "item_revenue": {
                        "$multiply": [
                            {"$toDouble": {"$ifNull": ["$itens.quantidade", 0]}},
                            {"$toDouble": {"$ifNull": ["$itens.price", 0]}},
                        ]
                    },
                    "item_cost": {
                        "$multiply": [
                            {"$toDouble": {"$ifNull": ["$itens.quantidade", 0]}},
                            {"$toDouble": {"$ifNull": ["$itens.cost", 0]}},
                        ]
                    },
                }
            },
            {
                "$facet": {
                    "daily": [
                        {"$match": {"order_date": {"$gte": daily_start, "$lt": daily_end}}},
                        {"$group": {"_id": None, "revenue": {"$sum": "$item_revenue"}, "cost": {"$sum": "$item_cost"}}},
                    ],
                    "monthly": [
                        {"$match": {"order_date": {"$gte": monthly_start, "$lt": monthly_end}}},
                        {"$group": {"_id": None, "revenue": {"$sum": "$item_revenue"}, "cost": {"$sum": "$item_cost"}}},
                    ],
                    "annual": [
                        {"$match": {"order_date": {"$gte": annual_start, "$lt": annual_end}}},
                        {"$group": {"_id": None, "revenue": {"$sum": "$item_revenue"}, "cost": {"$sum": "$item_cost"}}},
                    ],
                    "all_time": [
                        {"$group": {"_id": None, "revenue": {"$sum": "$item_revenue"}, "cost": {"$sum": "$item_cost"}}},
                    ],
                }
            },
        ]

        results = list(collection.aggregate(pipeline))

        def extract(facet_list: list) -> dict:
            if facet_list:
                r = float(facet_list[0].get("revenue") or 0)
                c = float(facet_list[0].get("cost") or 0)
                return {"revenue": r, "cost": c, "profit": r - c}
            return {"revenue": 0.0, "cost": 0.0, "profit": 0.0}

        if not results:
            empty = {"revenue": 0.0, "cost": 0.0, "profit": 0.0}
            return {"daily": empty, "monthly": empty, "annual": empty, "all_time": empty}

        facets = results[0]
        return {
            "daily": extract(facets.get("daily", [])),
            "monthly": extract(facets.get("monthly", [])),
            "annual": extract(facets.get("annual", [])),
            "all_time": extract(facets.get("all_time", [])),
        }


    def update_product_values_in_orders(self, product_name: str, sale_price: float, cost: float) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        result = collection.update_many(
            {
                "deleted": {"$ne": True},
                "itens": {
                    "$elemMatch": {
                        "item": product_name
                    }
                }
            },
            {
                "$set": {
                    "itens.$[elem].price": sale_price,
                    "itens.$[elem].cost": cost
                }
            },
            array_filters=[
                {"elem.item": product_name}
            ]
        )

        return result.modified_count