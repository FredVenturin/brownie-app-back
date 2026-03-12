from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class RestoreClient:

    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            client_id = http_request.path_params["client_id"]

            restored = self.__clients_repository.restore(client_id)

            if not restored:
                return HttpResponse(
                    body={
                        "error": "Cliente não encontrado na lixeira ou não pôde ser restaurado"
                    },
                    status_code=404
                )

            return HttpResponse(
                body={
                    "data": {
                        "type": "client",
                        "count": 1,
                        "attributes": {
                            "message": "Cliente restaurado com sucesso"
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)