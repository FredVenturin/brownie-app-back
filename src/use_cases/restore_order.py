from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class RestoreOrder:

    def __init__(self, orders_repository):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            order_id = http_request.path_params["order_id"]

            restored = self.__orders_repository.restore_registry(order_id)

            if not restored:
                return HttpResponse(
                    body={
                        "error": "Pedido não encontrado na lixeira ou não pôde ser restaurado"
                    },
                    status_code=404
                )

            return HttpResponse(
                body={
                    "data": {
                        "type": "order",
                        "count": 1,
                        "attributes": {
                            "message": "Pedido restaurado com sucesso"
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)