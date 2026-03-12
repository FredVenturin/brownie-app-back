from src.use_cases.restore_product import RestoreProduct
from src.models.repository.products_repository import ProductsRepository
from src.models.connection.connection_handler import db_connection_handler


def restore_product_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ProductsRepository(conn)
    use_case = RestoreProduct(repository)
    return use_case