from flask import Blueprint, request, jsonify, render_template
from app.model import model_instance
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/convert', methods=['POST'])
def predict_endpoint():
    # Kiểm tra xem request có chứa JSON không
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if 'queries' not in data:
        return jsonify({"error": "Missing 'text' field in request"}), 400

    queries = data['queries']
    prompt = data['prompt']

    result = model_instance.predict(prompt)
    print(result["result"])

    # forward to server nsga2
    server_nsga2_url = 'https://b173-2401-d800-7419-3a7f-abf2-4c40-cf04-4607.ngrok-free.app/api/schedule'
    response_from_server_nsga2 = requests.post(server_nsga2_url, json={'queries': queries, 'prompt': result["result"]})
    ans = response_from_server_nsga2.json()

    message = ans.get("message", "No message available")
    schedules = ans.get("schedules", [])

    return jsonify({
        "message": message,
        "schedules": schedules
    })

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "model_loaded": model_instance.model is not None
    })

@main_bp.route('/', methods=['GET'])
def home():
    """Trang chủ"""
    return render_template('index.html')
