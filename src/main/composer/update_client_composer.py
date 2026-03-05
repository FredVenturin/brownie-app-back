from src.use_cases.update_client import UpdateClient
from src.models.repository.clients_repository import ClientsRepository
from src.models.connection.connection_handler import db_connection_handler


def update_client_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ClientsRepository(conn)
    use_case = UpdateClient(repository)
    return use_case