from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from app.config.database_configuration import get_database
from app.config.embedding_model import load_model
from app.service.constraints_service import run_nsga_ii

app = Flask(__name__)
CORS(app)

# Gọi hàm để lấy database
db = get_database()
collection = db["ly_courses"]
# Load mô hình
model = load_model()

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    queries = data.get("queries", [])  # Nhận danh sách nhiều môn học
    top_k = data.get("top_k", 20)

    if not queries:
        return jsonify({"error": "Missing queries"}), 400

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
            {
                "$project": {
                    "_id": 0,
                    "Tên học phần": 1,
                    "Giảng viên": 1,
                    "Thứ": 1,
                    "Tiết": 1,
                    "Khu vực": 1,
                    "Số phòng": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        results = list(collection.aggregate(pipeline))
        print(pipeline)
        print("Results:", results)

        # Định dạng kết quả - giữ lại tất cả các lớp khác nhau
        formatted_results = []

        for item in results:
            # Chuyển đổi chuỗi Tiết thành list số nếu cần
            try:
                tiets = eval(item["Tiết"]) if isinstance(item["Tiết"], str) else item["Tiết"]
                # import ast
                # tiets = ast.literal_eval(item["Tiết"]) if isinstance(item["Tiết"], str) else item["Tiết"]
            except:
                tiets = []

            course_info = (
                item["Giảng viên"],
                item["Thứ"],
                tiets,
                item["Khu vực"],
                item["Số phòng"]
            )
            formatted_results.append(course_info)

        if formatted_results:
            courses_data[query] = formatted_results
        else:
            courses_data[query] = [("Không tìm thấy", "", [], "", "")]

    # ⚙️ Gọi hàm NSGA-II
    schedules = run_nsga_ii(courses_data)

    return jsonify({
            "schedules": schedules,
            "message": "Đã sắp xếp thành công"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
