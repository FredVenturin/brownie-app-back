from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class RestoreProduct:

    def __init__(self, products_repository):
        self.__products_repository = products_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            product_id = http_request.path_params["product_id"]

            restored = self.__products_repository.restore(product_id)

            if not restored:
                return HttpResponse(
                    body={
                        "error": "Produto não encontrado na lixeira ou não pôde ser restaurado"
                    },
                    status_code=404
                )

            return HttpResponse(
                body={
                    "data": {
                        "type": "product",
                        "count": 1,
                        "attributes": {
                            "message": "Produto restaurado com sucesso"
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)