from src.main.http_types.http_response import HttpResponse
from .types.http_unprocessable_entity import HttpUnprocessableEntityError
from .types.http_not_found import HttpNotFoundError

import traceback

def error_handler(error: Exception) -> HttpResponse:
    # 🔥 ISSO FAZ O RENDER MOSTRAR O ERRO NO LOG
    print("========== ERROR ==========")
    print(f"Type: {type(error).__name__}")
    print(f"Message: {str(error)}")
    print("Traceback:")
    print(traceback.format_exc())
    print("======== END ERROR ========")

    if isinstance(error, (HttpNotFoundError, HttpUnprocessableEntityError)):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )

    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )