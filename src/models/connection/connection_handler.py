import os
from pymongo import MongoClient

SEVEN_DAYS_IN_SECONDS = 7 * 24 * 60 * 60


class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.__database_name = os.getenv("DB_NAME", "rocket_db")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_string, serverSelectionTimeoutMS=5000)
        self.__db_connection = self.__client[self.__database_name]
        self.__client.server_info()
        self.__ensure_indexes()

    def __ensure_indexes(self):
        for collection_name in ["orders", "clients", "products"]:
            collection = self.__db_connection[collection_name]
            collection.create_index(
                "deleted_at",
                expireAfterSeconds=SEVEN_DAYS_IN_SECONDS,
                partialFilterExpression={
                    "deleted": True,
                    "deleted_at": {"$type": "date"}
                }
            )

    def get_db_connection(self):
        if self.__db_connection is None:
            self.connect_to_db()
        return self.__db_connection


db_connection_handler = DBConnectionHandler()