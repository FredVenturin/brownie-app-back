from src.use_cases.delete_product import DeleteProduct
from src.models.repository.products_repository import ProductsRepository
from src.models.connection.connection_handler import db_connection_handler


def delete_product_composer():
    conn = db_connection_handler.get_db_connection()
    repository = ProductsRepository(conn)
    use_case = DeleteProduct(repository)
    return use_case