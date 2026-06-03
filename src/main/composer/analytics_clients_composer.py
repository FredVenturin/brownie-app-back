from src.use_cases.analytics_clients import AnalyticsClients
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def analytics_clients_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = AnalyticsClients(repository)
    return use_case
