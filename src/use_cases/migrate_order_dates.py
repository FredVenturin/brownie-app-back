from datetime import datetime, time
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class MigrateOrderDates:
    def __init__(self, orders_repository):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Busca pedidos que tenham order_date como string (ou qualquer coisa não-datetime)
            orders = self.__orders_repository.select_many({"order_date": {"$type": "string"}})

            updated = 0
            for o in orders:
                oid = str(o.get("_id"))
                raw = o.get("order_date")

                if isinstance(raw, str) and raw.strip():
                    try:
                        d = datetime.strptime(raw.strip(), "%Y-%m-%d").date()
                        new_dt = datetime.combine(d, time.min)
                        ok = self.__orders_repository.edit_registry(oid, {"order_date": new_dt})
                        if ok:
                            updated += 1
                    except Exception:
                        # se tiver formato diferente, ignora
                        continue

            return HttpResponse(
                body={
                    "data": {
                        "attributes": {
                            "matched": len(orders),
                            "updated": updated
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)