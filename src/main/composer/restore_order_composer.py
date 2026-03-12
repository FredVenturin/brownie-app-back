from src.use_cases.restore_order import RestoreOrder
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def restore_order_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = RestoreOrder(repository)
    return use_case