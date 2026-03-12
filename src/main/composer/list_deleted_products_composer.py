from src.use_cases.list_deleted_products import ListDeletedProducts
from src.models.repository.products_repository import ProductsRepository
from src.models.connection.connection_handler import db_connection_handler


def list_deleted_products_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ProductsRepository(conn)
    use_case = ListDeletedProducts(repository)
    return use_case