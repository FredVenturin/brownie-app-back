from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class CreateClient:

    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            data = body.get("data", {})

            name = data.get("name")
            phone = data.get("phone")

            if not name:
                return HttpResponse(
                    body={"error": "name é obrigatório"},
                    status_code=400
                )

            client_id = self.__clients_repository.insert(name=name, phone=phone)

            return HttpResponse(
                body={
                    "data": {
                        "id": client_id
                    }
                },
                status_code=201
            )

        except Exception as exception:
            return error_handler(exception)