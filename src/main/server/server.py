from flask import Flask
from src.main.routes.delivery_routes import delivery_routes_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.register_blueprint(delivery_routes_bp)


@app.get("/")
def health():
    return {
        "ok": True,
        "service": "orders-api",
        "status": "running"
    }, 200