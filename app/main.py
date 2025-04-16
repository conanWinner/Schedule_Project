from flask import Flask
from flask_cors import CORS
from app.config.database_configuration import get_database
from app.config.embedding_model import load_model
from app.api.schedule_api import schedule_bp
from app.api.search_api import search_bp
from app.api.list_all_api import list_all_bp
app = Flask(__name__)
CORS(app)

# Khởi tạo DB và model
app.db = get_database()
app.model = load_model()

# Đăng ký blueprint cho từng nhóm endpoint
app.register_blueprint(schedule_bp, url_prefix='/api')
app.register_blueprint(search_bp, url_prefix='/api')
app.register_blueprint(list_all_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
