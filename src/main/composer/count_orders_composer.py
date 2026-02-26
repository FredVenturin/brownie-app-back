from src.use_cases.count_orders import CountOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def count_orders_composer():

    conn = db_connection_handler.get_db_connection()

    repository = OrdersRepository(conn)

    use_case = CountOrders(repository)

    return use_case