from src.use_cases.delete_many_orders import DeleteManyOrders
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler



def delete_many_order_composer():
    conn = db_connection_handler.get_db_connection()
    model = OrdersRepository(conn)
    use_case = DeleteManyOrders(model)

    return use_case