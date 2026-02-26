from src.use_cases.search_with_pagination import ListOrdersPaginated
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def search_with_pagination_composer():

    conn = db_connection_handler.get_db_connection()

    repository = OrdersRepository(conn)

    use_case = ListOrdersPaginated(repository)

    return use_case