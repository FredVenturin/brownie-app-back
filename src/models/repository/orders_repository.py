class OrdersRepository:
    def __init__(self, db_connection) ->None:
        self.__collection_name = "orders"
        self.__db_connection = db_connection

    def insert_document(self, document:dict) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(document)

    def insert_list_of_documents(self, list_of_documents: list) ->None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_many(list_of_documents)
