from datetime import datetime, timedelta
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ProfitSelectedPeriod:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}

            year_raw = qp.get("year")
            month_raw = qp.get("month")
            day_raw = qp.get("day")

            if not year_raw:
                return HttpResponse(
                    body={"error": "Query param 'year' é obrigatório (ex: ?year=2025)."},
                    status_code=400,
                )

            year = int(year_raw)
            month = int(month_raw) if month_raw not in (None, "", "null") else None
            day = int(day_raw) if day_raw not in (None, "", "null") else None

            if month is not None and (month < 1 or month > 12):
                return HttpResponse(body={"error": "month deve ser 1..12"}, status_code=400)
            if day is not None and (day < 1 or day > 31):
                return HttpResponse(body={"error": "day deve ser 1..31"}, status_code=400)

            # define range [start, end)
            if month is None:
                start = datetime(year, 1, 1, 0, 0, 0)
                end = datetime(year + 1, 1, 1, 0, 0, 0)
                label = f"{year}"
            elif day is None:
                start = datetime(year, month, 1, 0, 0, 0)
                if month == 12:
                    end = datetime(year + 1, 1, 1, 0, 0, 0)
                else:
                    end = datetime(year, month + 1, 1, 0, 0, 0)
                label = f"{year}-{month:02d}"
            else:
                start = datetime(year, month, day, 0, 0, 0)
                end = start + timedelta(days=1)
                label = f"{year}-{month:02d}-{day:02d}"

            doc_filter = {
                "status": "sold",
                "order_date": {"$gte": start, "$lt": end},
            }

            projection = {
                "_id": 0,
                "itens.quantidade": 1,
                "itens.price": 1,
                "itens.cost": 1,
            }

            orders = self.__orders_repository.select_many_with_properties(doc_filter, projection)

            revenue = 0.0
            cost = 0.0

            for o in orders:
                itens = o.get("itens") or []

                order_revenue = 0.0
                order_cost = 0.0

                for it in itens:
                    qtd = float(it.get("quantidade") or 0)
                    price = float(it.get("price") or 0)
                    cst = float(it.get("cost") or 0)

                    order_revenue += qtd * price
                    order_cost += qtd * cst

                revenue += order_revenue
                cost += order_cost

            result = {"revenue": revenue, "cost": cost, "profit": revenue - cost}

            return HttpResponse(
                body={
                    "data": {
                        "attributes": {
                            "period": {
                                "label": label,
                                "start": start.isoformat(),
                                "end": end.isoformat(),
                            },
                            "result": result,
                        }
                    }
                },
                status_code=200,
            )

        except Exception as exception:
            return error_handler(exception)