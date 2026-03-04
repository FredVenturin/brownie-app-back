from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ListClients:

    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            clients = self.__clients_repository.list_all()

            return HttpResponse(
                body={
                    "data": {
                        "attributes": clients
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)