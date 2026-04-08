from src.use_cases.orders_stats import OrdersStats
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def orders_stats_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = OrdersStats(repository)
    return use_case
