from src.use_cases.restore_client import RestoreClient
from src.models.repository.clients_repository import ClientsRepository
from src.models.connection.connection_handler import db_connection_handler


def restore_client_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ClientsRepository(conn)
    use_case = RestoreClient(repository)
    return use_case