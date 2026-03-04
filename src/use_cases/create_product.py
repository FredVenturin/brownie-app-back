from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse


class CreateProduct:
    def __init__(self, products_repository):
        self.__products_repository = products_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body["data"]

        name = body["name"]
        sale_price = body["sale_price"]
        cost = body["cost"]

        product_id = self.__products_repository.insert(
            name=name,
            sale_price=sale_price,
            cost=cost
        )

        return HttpResponse(
            status_code=201,
            body={
                "data": {
                    "id": product_id
                }
            }
        )