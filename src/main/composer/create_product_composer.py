from src.use_cases.create_product import CreateProduct
from src.models.repository.products_repository import ProductsRepository
from src.models.connection.connection_handler import db_connection_handler


def create_product_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ProductsRepository(conn)
    use_case = CreateProduct(repository)
    return use_case