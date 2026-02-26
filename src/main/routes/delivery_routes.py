from flask import Blueprint, jsonify, request
from src.main.http_types.http_request import HttpRequest

from src.main.composer.registry_order_composer import registry_order_composer
from src.main.composer.registry_finder_composer import registry_finder_composer
from src.main.composer.registry_updater_composer import registry_updater_composer
from src.main.composer.list_of_orders_composer import list_of_orders_composer
from src.main.composer.delete_order_composer import delete_order_composer
from src.main.composer.update_order_status_composer import update_order_status_composer

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

@delivery_routes_bp.route("/delivery/order", methods=["GET"])
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


