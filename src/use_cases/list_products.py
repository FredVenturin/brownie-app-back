from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse


class ListProducts:
    def __init__(self, products_repository):
        self.__products_repository = products_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        products = self.__products_repository.list_all()

        return HttpResponse(
            status_code=200,
            body={
                "data": {
                    "attributes": products
                }
            }
        )