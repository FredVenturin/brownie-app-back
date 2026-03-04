from src.use_cases.profit_summary import ProfitSummary
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def profit_summary_composer():
    conn = db_connection_handler.get_db_connection()
    repository = OrdersRepository(conn)
    use_case = ProfitSummary(repository)
    return use_case