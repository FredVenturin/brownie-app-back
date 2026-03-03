import os
from pymongo import MongoClient

class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.__database_name = os.getenv("DB_NAME", "rocket_db")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        # timeout pra não ficar pendurado
        self.__client = MongoClient(self.__connection_string, serverSelectionTimeoutMS=5000)
        self.__db_connection = self.__client[self.__database_name]
        # força conexão agora (pra erro aparecer no log)
        self.__client.server_info()

    def get_db_connection(self):
        if self.__db_connection is None:
            self.connect_to_db()
        return self.__db_connection

db_connection_handler = DBConnectionHandler()