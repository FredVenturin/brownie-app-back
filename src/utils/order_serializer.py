def serialize_order(order: dict) -> dict:
    if not order:
        return order

    # id
    if "_id" in order:
        order["_id"] = str(order["_id"])

    # datas (datetime -> string ISO)
    for key in ("created_at", "order_date", "sold_at"):
        if key in order and order[key] is not None:
            val = order[key]
            if hasattr(val, "isoformat"):
                order[key] = val.isoformat()

    return order