from src.use_cases.list_of_orders import ListOfOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler



def list_of_orders_composer():
    conn = db_connection_handler.get_db_connection()
    model = OrdersRepository(conn)
    use_case = ListOfOrders(model)

    return use_case