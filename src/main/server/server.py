from flask import Flask, jsonify

from src.main.routes.delivery_routes import delivery_routes_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(delivery_routes_bp)
print("=== ROTAS CARREGADAS ===")
print(app.url_map)
print("========================")
@app.get("/")
def health():
    return {"ok": True, "service": "orders-api"}, 200

@app.get("/health")
def health():
    return jsonify({"ok": True}), 200

