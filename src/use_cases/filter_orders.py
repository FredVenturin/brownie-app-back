from datetime import datetime, time, timedelta
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler
from src.utils.order_serializer import serialize_order


class FilterOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def filters(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}

            page = int(qp.get("page", 1))
            limit = int(qp.get("limit", 10))

            doc_filter = self.__build_doc_filter(qp)

            orders = self.__orders_repository.select_with_pagination(
                doc_filter, page, limit
            )

            total = self.__orders_repository.count_documents(doc_filter)
            has_next = (page * limit) < total

            orders = [serialize_order(o) for o in orders]

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "attributes": orders
                    },
                    "meta": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "has_next": has_next
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)

    def __parse_date(self, s: str) -> datetime:
        return datetime.strptime(s, "%Y-%m-%d")

    def __build_doc_filter(self, qp: dict) -> dict:
        doc_filter = {}

        status = qp.get("status")
        name = qp.get("name")
        product = qp.get("product")
        start_date = qp.get("start_date")
        end_date = qp.get("end_date")

        if status:
            doc_filter["status"] = status

        if name:
            doc_filter["name"] = {"$regex": name, "$options": "i"}

        if product:
            doc_filter["itens.item"] = {"$regex": product, "$options": "i"}

        # ✅ Filtrando por order_date (data do pedido)
        if start_date or end_date:
            # Caso: usuário preencheu só start ou só end
            if start_date and not end_date:
                d = self.__parse_date(start_date).date()
                doc_filter["order_date"] = {
                    "$gte": datetime.combine(d, time.min)
                }

            elif end_date and not start_date:
                d = self.__parse_date(end_date).date()
                # pega tudo até o final do dia
                doc_filter["order_date"] = {
                    "$lte": datetime.combine(d, time.max)
                }

            else:
                # Caso: os dois preenchidos
                if start_date == end_date:
                    # ✅ um único dia: [00:00, próximo dia 00:00)
                    d = self.__parse_date(start_date).date()
                    start_dt = datetime.combine(d, time.min)
                    end_dt = start_dt + timedelta(days=1)

                    doc_filter["order_date"] = {
                        "$gte": start_dt,
                        "$lt": end_dt
                    }
                else:
                    # ✅ intervalo: [start 00:00, end 23:59:59.999...]
                    ds = self.__parse_date(start_date).date()
                    de = self.__parse_date(end_date).date()

                    doc_filter["order_date"] = {
                        "$gte": datetime.combine(ds, time.min),
                        "$lte": datetime.combine(de, time.max),
                    }

        return doc_filter