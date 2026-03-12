from src.use_cases.list_deleted_clients import ListDeletedClients
from src.models.repository.clients_repository import ClientsRepository
from src.models.connection.connection_handler import db_connection_handler


def list_deleted_clients_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ClientsRepository(conn)
    use_case = ListDeletedClients(repository)
    return use_case