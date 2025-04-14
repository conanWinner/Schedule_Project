from flask import Blueprint, request, jsonify, current_app
from app.service.constraints_service import run_nsga_ii

schedule_bp = Blueprint("schedule", __name__)

@schedule_bp.route("/schedule", methods=["POST"])
def schedule():
    data = request.json
    queries = data.get("queries", [])
    top_k = data.get("top_k", 20)

    if not queries:
        return jsonify({"error": "Missing queries"}), 400

    collection = current_app.db["ly_courses"]
    model = current_app.model

    courses_data = {}

    for query in queries:
        query_vector = model.encode(query).tolist()

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 1000,
                    "limit": top_k
                }
            },
            {"$unset": "embedding"},
            {"$project": {...}}
        ]

        results = list(collection.aggregate(pipeline))

        formatted_results = []
        for item in results:
            tiets = eval(item["Tiết"]) if isinstance(item["Tiết"], str) else item["Tiết"]
            course_info = {...}  # giống như trước
            formatted_results.append(course_info)

        courses_data[query] = formatted_results or [("Không tìm thấy", "", "", "", "", "", "", [], "", "", "")]

    schedules = run_nsga_ii(courses_data)

    return jsonify({"schedules": schedules, "message": "Đã sắp xếp thành công"})



