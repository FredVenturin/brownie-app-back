from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class UpdateProduct:
    def __init__(self, products_repository, orders_repository):
        self.__products_repository = products_repository
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            product_id = (http_request.path_params or {}).get("product_id")
            if not product_id:
                return HttpResponse(body={"error": "product_id é obrigatório"}, status_code=400)

            body = http_request.body or {}
            data = body.get("data") or {}

            name = data.get("name")
            sale_price = data.get("sale_price")
            cost = data.get("cost")

            update_fields = {}

            if name is not None:
                update_fields["name"] = str(name).strip()

            if sale_price is not None:
                update_fields["sale_price"] = float(sale_price)

            if cost is not None:
                update_fields["cost"] = float(cost)

            if not update_fields:
                return HttpResponse(
                    body={"error": "Envie ao menos um campo para atualizar (name, sale_price, cost)."},
                    status_code=400
                )

            current_product = self.__products_repository.find_by_id(product_id)

            if not current_product:
                return HttpResponse(body={"error": "Produto não encontrado."}, status_code=404)

            updated = self.__products_repository.update(product_id, update_fields)

            if not updated:
                return HttpResponse(body={"error": "Produto não encontrado."}, status_code=404)

            final_name = update_fields.get("name", current_product.get("name"))
            final_sale_price = update_fields.get("sale_price", current_product.get("sale_price"))
            final_cost = update_fields.get("cost", current_product.get("cost"))

            self.__orders_repository.update_product_values_in_orders(
                current_product.get("name"),
                final_sale_price,
                final_cost
            )

            return HttpResponse(
                body={
                    "data": {
                        "type": "Product",
                        "id": product_id,
                        "updated": True,
                        "propagated_to_orders": True,
                        "final_name": final_name,
                        "final_sale_price": final_sale_price,
                        "final_cost": final_cost
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)