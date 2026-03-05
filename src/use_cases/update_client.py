from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class UpdateClient:
    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            client_id = (http_request.path_params or {}).get("client_id")
            if not client_id:
                return HttpResponse(body={"error": "client_id é obrigatório"}, status_code=400)

            body = http_request.body or {}
            data = body.get("data") or {}

            name = data.get("name")
            phone = data.get("phone")

            update_fields = {}

            if name is not None:
                update_fields["name"] = str(name).strip()

            if phone is not None:
                phone_str = str(phone).strip()
                update_fields["phone"] = phone_str if phone_str else None

            if not update_fields:
                return HttpResponse(
                    body={"error": "Envie ao menos um campo para atualizar (name/phone)."},
                    status_code=400
                )

            updated = self.__clients_repository.update(client_id, update_fields)

            if not updated:
                return HttpResponse(body={"error": "Cliente não encontrado."}, status_code=404)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Client",
                        "id": client_id,
                        "updated": True
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)