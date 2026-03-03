from flask import Flask, jsonify
from flask_cors import CORS
from src.main.routes.delivery_routes import delivery_routes_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(delivery_routes_bp)

@app.get("/")
def home():
    return {"ok": True, "service": "orders-api"}, 200

@app.get("/health")
def health():
    return jsonify({"ok": True}), 200