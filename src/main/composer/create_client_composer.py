from src.use_cases.create_client import CreateClient
from src.models.repository.clients_repository import ClientsRepository
from src.models.connection.connection_handler import db_connection_handler


def create_client_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ClientsRepository(conn)
    use_case = CreateClient(repository)
    return use_case