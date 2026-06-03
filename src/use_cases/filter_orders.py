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

            parsed = self.__parse_params(qp)
            doc_filter = self.__build_doc_filter(parsed)

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
                        "has_next": has_next,
                        "filters": {
                            "status": parsed["statuses"] or None,
                            "name": parsed["names"] or None,
                            "product": parsed["products"] or None,
                            "start_date": parsed["start_date"],
                            "end_date": parsed["end_date"],
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)

    def __split(self, raw: str) -> list:
        return [v.strip() for v in raw.split(",") if v.strip()]

    def __parse_date(self, s: str) -> datetime:
        return datetime.strptime(s, "%Y-%m-%d")

    def __parse_params(self, qp: dict) -> dict:
        return {
            "statuses": self.__split(qp.get("status", "")),
            "names": self.__split(qp.get("name", "")),
            "products": self.__split(qp.get("product", "")),
            "start_date": qp.get("start_date"),
            "end_date": qp.get("end_date"),
        }

    def __build_doc_filter(self, p: dict) -> dict:
        doc_filter = {}

        if p["statuses"]:
            statuses = p["statuses"]
            doc_filter["status"] = {"$in": statuses} if len(statuses) > 1 else statuses[0]

        if p["names"]:
            names = p["names"]
            if len(names) > 1:
                doc_filter["name"] = {"$in": names}
            else:
                doc_filter["name"] = {"$regex": names[0], "$options": "i"}

        if p["products"]:
            products = p["products"]
            doc_filter["itens.item"] = {"$in": products} if len(products) > 1 else products[0]

        start_date = p["start_date"]
        end_date = p["end_date"]

        if start_date or end_date:
            if start_date and not end_date:
                d = self.__parse_date(start_date).date()
                doc_filter["order_date"] = {"$gte": datetime.combine(d, time.min)}

            elif end_date and not start_date:
                d = self.__parse_date(end_date).date()
                doc_filter["order_date"] = {"$lte": datetime.combine(d, time.max)}

            elif start_date == end_date:
                d = self.__parse_date(start_date).date()
                start_dt = datetime.combine(d, time.min)
                doc_filter["order_date"] = {"$gte": start_dt, "$lt": start_dt + timedelta(days=1)}

            else:
                ds = self.__parse_date(start_date).date()
                de = self.__parse_date(end_date).date()
                doc_filter["order_date"] = {
                    "$gte": datetime.combine(ds, time.min),
                    "$lte": datetime.combine(de, time.max),
                }

        return doc_filter