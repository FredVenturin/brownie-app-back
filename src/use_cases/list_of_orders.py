from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler


class ListOfOrders:
    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def find_list(self, http_request: HttpRequest) -> HttpResponse:
        try:
            orders = self.__search_orders()
            return self.__format_response(orders)    
        except Exception as exception:
            return error_handler(exception)

    def __search_orders(self)->list:
        orders_cursor = self.__orders_repository.select_many({})
        orders = list(orders_cursor)

        if not orders: 
            raise HttpNotFoundError("Orders not found")
        
        for order in orders:
            order["_id"] = str(order["_id"])

        return orders
    
    def __format_response(self, orders: list) -> HttpResponse: 

        return HttpResponse(
            body={
                "data": {
                    "count": len(orders),
                    "type": "Orders",
                    "attributes": orders
                }
            },
            status_code=200
        )
