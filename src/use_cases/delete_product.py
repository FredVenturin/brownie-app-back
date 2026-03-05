from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class DeleteProduct:
    def __init__(self, products_repository):
        self.__products_repository = products_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            product_id = (http_request.path_params or {}).get("product_id")
            if not product_id:
                return HttpResponse(body={"error": "product_id é obrigatório"}, status_code=400)

            deleted = self.__products_repository.delete(product_id)

            if not deleted:
                return HttpResponse(body={"error": "Produto não encontrado."}, status_code=404)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Product",
                        "id": product_id,
                        "deleted": True
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)