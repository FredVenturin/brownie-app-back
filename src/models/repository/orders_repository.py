from bson.objectid import ObjectId
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface

class OrdersRepository(OrdersRepositoryInterface):
    def __init__(self, db_connection) ->None:
        self.__collection_name = "orders"
        self.__db_connection = db_connection

    def insert_document(self, document:dict) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(document)

    def insert_list_of_documents(self, list_of_documents: list) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_many(list_of_documents)

    def select_many(self, doc_filter: dict) ->list:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(doc_filter)
        return data
    
    def select_one(self, doc_filter:dict) ->dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        response = collection.find_one(doc_filter)
        return response
    
    def select_many_with_properties(self, doc_filter: dict) ->list:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(
            doc_filter,
            { "_id": 0, "cupom": 0}
        )
        return data
    
    def select_if_property_exists(self) ->dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        response = collection.find_one(
            {"address": {"$exists": True}},
            { "_id": 0, "cupom": 0}
        )
        return response
    
    def select_by_object_id(self, object_id: str) ->dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find_one({"_id": ObjectId(object_id)})
        return data
    
    def edit_registry(self, order_id:str, update_fields: dict) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_fields}
        )

    def edit_many_registries(self) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.update_many(
            {"itens.refrigerante": {"$exists": True}},
            {"$set": {"itens.pizza.quantidade": 30}}
        )

    def edit_registry_with_increment(self) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.update_many(
            {"itens.refrigerante": {"$exists": True}},
            {"$inc": {"itens.pizza.quantidade": 50}}
        )

    def delete_registry(self) ->None:
        collection = collection = self.__db_connection.get_collection(self.__collection_name)
        collection.delete_one({"_id": ObjectId("698e2c13a65185533a153bde")})

    def delete_many_registries(self) ->None:
        collection = collection = self.__db_connection.get_collection(self.__collection_name)
        collection.delete_many({"itens.refrigerante": {"$exists": True}})

