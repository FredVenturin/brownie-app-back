from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class DeleteClient:
    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            client_id = (http_request.path_params or {}).get("client_id")
            if not client_id:
                return HttpResponse(body={"error": "client_id é obrigatório"}, status_code=400)

            deleted = self.__clients_repository.delete(client_id)

            if not deleted:
                return HttpResponse(body={"error": "Cliente não encontrado."}, status_code=404)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Client",
                        "id": client_id,
                        "deleted": True
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)