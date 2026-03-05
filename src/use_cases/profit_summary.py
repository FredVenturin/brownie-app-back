from datetime import datetime, timedelta
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ProfitSummary:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            now = datetime.now()

            daily_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            daily_end = daily_start + timedelta(days=1)

            monthly_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if monthly_start.month == 12:
                monthly_end = monthly_start.replace(year=monthly_start.year + 1, month=1)
            else:
                monthly_end = monthly_start.replace(month=monthly_start.month + 1)

            annual_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            annual_end = annual_start.replace(year=annual_start.year + 1)

            def calc_from_orders(orders: list) -> dict:
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

                return {
                    "revenue": revenue,
                    "cost": cost,
                    "profit": revenue - cost,
                }

            def calc_range(dt_start: datetime, dt_end: datetime) -> dict:
                doc_filter = {
                    "status": "sold",
                    "order_date": {"$gte": dt_start, "$lt": dt_end},
                }

                projection = {
                    "_id": 0,
                    "itens.quantidade": 1,
                    "itens.price": 1,
                    "itens.cost": 1,
                }

                orders = self.__orders_repository.select_many_with_properties(doc_filter, projection)
                return calc_from_orders(orders)

            def calc_all_time() -> dict:
                doc_filter = {
                    "status": "sold",
                }

                projection = {
                    "_id": 0,
                    "itens.quantidade": 1,
                    "itens.price": 1,
                    "itens.cost": 1,
                }

                orders = self.__orders_repository.select_many_with_properties(doc_filter, projection)
                return calc_from_orders(orders)

            return HttpResponse(
                body={
                    "data": {
                        "attributes": {
                            "daily": calc_range(daily_start, daily_end),
                            "monthly": calc_range(monthly_start, monthly_end),
                            "annual": calc_range(annual_start, annual_end),
                            "all_time": calc_all_time(),
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)