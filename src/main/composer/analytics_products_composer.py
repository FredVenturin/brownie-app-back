from src.use_cases.analytics_products import AnalyticsProducts
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def analytics_products_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = AnalyticsProducts(repository)
    return use_case
