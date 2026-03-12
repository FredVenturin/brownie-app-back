from src.use_cases.filter_deleted_orders import FilterDeletedOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def filter_deleted_orders_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = FilterDeletedOrders(repository)
    return use_case