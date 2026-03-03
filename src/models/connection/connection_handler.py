import os
from pymongo import MongoClient


class DBConnectionHandler:
    def __init__(self):
        # tenta pegar do ambiente (Render / produção)
        self.__connection_string = os.getenv(
            "MONGO_URI",
            "mongodb://localhost:27017/"
        )

        self.__database_name = os.getenv(
            "DB_NAME",
            "rocket_db"
        )

        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        if not self.__db_connection:
            self.connect_to_db()
        return self.__db_connection


db_connection_handler = DBConnectionHandler()