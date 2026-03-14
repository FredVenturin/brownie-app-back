from src.use_cases.update_product import UpdateProduct
from src.models.repository.products_repository import ProductsRepository
from src.models.repository.orders_repository import OrdersRepository
from src.models.connection.connection_handler import db_connection_handler


def update_product_composer():
    conn = db_connection_handler.get_db_connection()
    products_repository = ProductsRepository(conn)
    orders_repository = OrdersRepository(conn)
    use_case = UpdateProduct(products_repository, orders_repository)
    return use_case