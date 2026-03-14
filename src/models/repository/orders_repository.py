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

        return list(collection.find(doc_filter))

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

        cursor = collection.find(doc_filter).skip(skip).limit(limit)
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

        cursor = collection.find(doc_filter).skip(skip).limit(limit)
        return list(cursor)
    
    def count_deleted_documents(self, doc_filter: dict) -> int:
        collection = self.__db_connection.get_collection(self.__collection_name)

        doc_filter["deleted"] = True

        return collection.count_documents(doc_filter)
    

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