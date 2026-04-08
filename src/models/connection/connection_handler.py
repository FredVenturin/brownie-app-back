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
        # TTL: auto-remove soft-deleted documents after 7 days
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

        # Performance indexes for orders
        orders = self.__db_connection["orders"]
        orders.create_index([("deleted", 1), ("status", 1)])
        orders.create_index([("deleted", 1), ("status", 1), ("order_date", -1)])
        orders.create_index([("deleted", 1), ("order_date", -1)])
        orders.create_index([("deleted", 1), ("name", 1)])

        # Performance indexes for clients and products (list sorted by name)
        self.__db_connection["clients"].create_index([("deleted", 1), ("name", 1)])
        self.__db_connection["products"].create_index([("deleted", 1), ("name", 1)])

    def get_db_connection(self):
        if self.__db_connection is None:
            self.connect_to_db()
        return self.__db_connection


db_connection_handler = DBConnectionHandler()