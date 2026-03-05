from src.use_cases.update_product import UpdateProduct
from src.models.repository.products_repository import ProductsRepository
from src.models.connection.connection_handler import db_connection_handler


def update_product_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ProductsRepository(conn)
    use_case = UpdateProduct(repository)
    return use_case