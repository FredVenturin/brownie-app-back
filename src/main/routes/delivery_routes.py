from flask import Blueprint, jsonify, request
from src.main.http_types.http_request import HttpRequest
from datetime import datetime, timedelta
from src.models.connection.connection_handler import db_connection_handler

from src.main.composer.registry_order_composer import registry_order_composer
from src.main.composer.registry_finder_composer import registry_finder_composer
from src.main.composer.registry_updater_composer import registry_updater_composer
from src.main.composer.list_of_orders_composer import list_of_orders_composer
from src.main.composer.delete_order_composer import delete_order_composer
from src.main.composer.update_order_status_composer import update_order_status_composer
from src.main.composer.search_with_pagination_composer import search_with_pagination_composer
from src.main.composer.count_orders_composer import count_orders_composer
from src.main.composer.delete_many_orders_composer import delete_many_order_composer
from src.main.composer.filter_orders_composer import filter_orders_composer
from src.main.composer.update_many_orders_composer import update_many_orders_composer
from src.main.composer.increment_orders_composer import increment_orders_composer

delivery_routes_bp = Blueprint("delivery_routes", __name__)

@delivery_routes_bp.route("/delivery/order", methods=["POST"])
def registry_order():
    user_case = registry_order_composer()
    http_request = HttpRequest(body= request.json)
    response = user_case.registry(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/order/<order_id>", methods=["GET"])
def registry_finder(order_id):
    user_case = registry_finder_composer()
    http_request = HttpRequest(path_params= {"order_id":order_id})
    response = user_case.find(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/order/<order_id>", methods=["PATCH"])
def registry_updater(order_id):
    user_case = registry_updater_composer()
    http_request = HttpRequest(path_params= {"order_id":order_id}, body= request.json)
    response = user_case.update(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/orders/all", methods=["GET"])
def list_orders():
    user_case = list_of_orders_composer()
    http_request = HttpRequest()
    response = user_case.find_list(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/order/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    user_case = delete_order_composer()
    http_request = HttpRequest(path_params= {"order_id":order_id})
    response = user_case.delete(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/order/<order_id>/status", methods=["PATCH"])
def update_status(order_id):
    use_case = update_order_status_composer()
    http_request = HttpRequest(
        path_params={"order_id": order_id},
        body=request.json
    )
    response = use_case.execute(http_request)

    return jsonify(response.body), response.status_code

from src.errors.error_handler import error_handler

@delivery_routes_bp.route("/delivery/orders", methods=["GET"])
def list_orders_paginated():
    try:
        use_case = search_with_pagination_composer()

        http_request = HttpRequest(
            query_params=request.args.to_dict()
        )

        response = use_case.execute(http_request)
        return jsonify(response.body), response.status_code

    except Exception as e:
        response = error_handler(e)
        return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/orders/count", methods=["GET"])
def count_orders():

    try:
        use_case = count_orders_composer()

        http_request = HttpRequest(
            query_params=request.args.to_dict()
        )

        response = use_case.execute(http_request)

        return jsonify(response.body), response.status_code

    except Exception as e:
        response = error_handler(e)
        return jsonify(response.body), response.status_code
    
    

@delivery_routes_bp.route("/delivery/orders/update-many", methods=["PATCH"])
def update_many_orders():

    use_case = update_many_orders_composer()

    http_request = HttpRequest(
        body=request.json
    )

    response = use_case.update_many(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/orders/increment", methods=["PATCH"])
def increment_orders():

    use_case = increment_orders_composer()

    http_request = HttpRequest(
        body=request.json
    )

    response = use_case.increment(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/orders/delete-many", methods=["DELETE"])
def delete_many_orders():

    use_case = delete_many_order_composer()

    http_request = HttpRequest(
        body=request.json
    )

    response = use_case.delete_many(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/orders/filter", methods=["GET"])
def filter_orders():

    use_case = filter_orders_composer()

    http_request = HttpRequest(
        query_params=request.args.to_dict()
    )

    response = use_case.filters(http_request)

    return jsonify(response.body), response.status_code

@delivery_routes_bp.route("/delivery/profit/summary", methods=["GET"])
def profit_summary():
    db = db_connection_handler.get_db_connection()
    collection = db.get_collection("orders")

    now = datetime.now()

    def start_of_day(dt: datetime) -> datetime:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def start_of_month(dt: datetime) -> datetime:
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def start_of_year(dt: datetime) -> datetime:
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def calc_range(dt_start: datetime, dt_end: datetime) -> dict:
        pipeline = [
            {
                "$match": {
                    "status": "sold",
                    "order_date": {"$gte": dt_start, "$lt": dt_end},
                }
            },
            {
                "$project": {
                    "revenue": {"$ifNull": ["$prices.total", 0]},
                    "cost": {
                        "$sum": {
                            "$map": {
                                "input": {"$ifNull": ["$itens", []]},
                                "as": "it",
                                "in": {
                                    "$multiply": [
                                        {"$ifNull": ["$$it.quantidade", 0]},
                                        {"$ifNull": ["$$it.cost", 0]},
                                    ]
                                },
                            }
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": None,
                    "revenue": {"$sum": "$revenue"},
                    "cost": {"$sum": "$cost"},
                }
            },
        ]

        result = list(collection.aggregate(pipeline))
        if not result:
            return {"revenue": 0, "cost": 0, "profit": 0}

        revenue = float(result[0].get("revenue", 0) or 0)
        cost = float(result[0].get("cost", 0) or 0)
        return {"revenue": revenue, "cost": cost, "profit": revenue - cost}

    daily_start = start_of_day(now)
    daily_end = daily_start + timedelta(days=1)

    monthly_start = start_of_month(now)
    monthly_end = (monthly_start.replace(month=monthly_start.month + 1) if monthly_start.month < 12 else monthly_start.replace(year=monthly_start.year + 1, month=1))

    annual_start = start_of_year(now)
    annual_end = annual_start.replace(year=annual_start.year + 1)

    return jsonify({
        "data": {
            "attributes": {
                "daily": calc_range(daily_start, daily_end),
                "monthly": calc_range(monthly_start, monthly_end),
                "annual": calc_range(annual_start, annual_end),
            }
        }
    }), 200