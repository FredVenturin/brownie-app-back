from src.use_cases.increment_orders import IncrementOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler



def increment_orders_composer():
    conn = db_connection_handler.get_db_connection()
    model = OrdersRepository(conn)
    use_case = IncrementOrders(model)

    return use_case