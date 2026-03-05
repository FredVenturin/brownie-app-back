from src.use_cases.migrate_order_dates import MigrateOrderDates
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def migrate_order_dates_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = MigrateOrderDates(repository)
    return use_case