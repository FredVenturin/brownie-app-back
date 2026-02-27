from src.use_cases.update_many_orders import UpdateManyOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler



def update_many_orders_composer():
    conn = db_connection_handler.get_db_connection()
    model = OrdersRepository(conn)
    use_case = UpdateManyOrders(model)

    return use_case