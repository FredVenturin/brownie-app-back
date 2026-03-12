from app import app
from src.models.connection.connection_handler import db_connection_handler


if __name__ == "__main__":
    db_connection_handler.connect_to_db()
    app.run(host="0.0.0.0", port=3000)