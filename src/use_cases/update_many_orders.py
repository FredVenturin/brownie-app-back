from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_handler import error_handler


class UpdateManyOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def update_many(self, http_request: HttpRequest) -> HttpResponse:

        try:

            body = http_request.body or {}

            filters = body.get("filter")
            update_data = body.get("update")

            if not filters:
                raise HttpUnprocessableEntityError("Missing 'filter' field")

            if not update_data:
                raise HttpUnprocessableEntityError("Missing 'update' field")


            modified_count = self.__update_orders(filters, update_data)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "modified": modified_count,
                        "message": "Orders updated successfully"
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)


    def __update_orders(self, filters: dict, update_data: dict) -> int:

        modified_count = self.__orders_repository.edit_many_registries(
            filters,
            update_data
        )

        if modified_count == 0:
            raise HttpNotFoundError("No orders were updated")

        return modified_count