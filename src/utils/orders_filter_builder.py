from datetime import datetime, time

ALLOWED_STATUSES = {"confirmed", "preparing", "sold", "cancelled"}

def _parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")

def build_orders_doc_filter(data: dict) -> dict:
    data = data or {}
    doc_filter = {}

    status = data.get("status")
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if status and status in ALLOWED_STATUSES:
        doc_filter["status"] = status

    if name:
        doc_filter["name"] = {"$regex": name, "$options": "i"}

    # 🔹 mesmo padrão do tópico 2 (filtrando por created_at)
    if start_date or end_date:
        doc_filter["created_at"] = {}

        if start_date:
            d = _parse_date(start_date).date()
            doc_filter["created_at"]["$gte"] = datetime.combine(d, time.min)

        if end_date:
            d = _parse_date(end_date).date()
            doc_filter["created_at"]["$lte"] = datetime.combine(d, time.max)

        if not doc_filter["created_at"]:
            del doc_filter["created_at"]

    return doc_filter