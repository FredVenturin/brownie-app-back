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

            summary = self.__orders_repository.aggregate_profit_summary(
                daily_start, daily_end,
                monthly_start, monthly_end,
                annual_start, annual_end,
            )

            return HttpResponse(
                body={"data": {"attributes": summary}},
                status_code=200,
            )

        except Exception as exception:
            return error_handler(exception)