from datetime import datetime, time, timedelta
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class AnalyticsProducts:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}
            start_date, end_date = self.__parse_date_range(qp)

            results = self.__orders_repository.aggregate_product_sales(
                start_date=start_date,
                end_date=end_date,
            )

            return HttpResponse(
                body={
                    "data": {"attributes": results},
                    "meta": {
                        "start_date": qp.get("start_date"),
                        "end_date": qp.get("end_date"),
                        "total_products": len(results),
                    }
                },
                status_code=200,
            )

        except Exception as exception:
            return error_handler(exception)

    def __parse_date_range(self, qp: dict):
        raw_start = qp.get("start_date")
        raw_end = qp.get("end_date")

        start_date = None
        end_date = None

        if raw_start:
            d = datetime.strptime(raw_start, "%Y-%m-%d").date()
            start_date = datetime.combine(d, time.min)

        if raw_end:
            d = datetime.strptime(raw_end, "%Y-%m-%d").date()
            end_date = datetime.combine(d, time.max)

        return start_date, end_date
