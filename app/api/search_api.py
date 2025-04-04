from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

# Kết nối MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["university_db"]
collection = db["courses"]

# Load mô hình Sentence Transformer để tạo embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    queries = data.get("queries", [])  # Nhận danh sách nhiều môn học
    top_k = data.get("top_k", 20)

    if not queries:
        return jsonify({"error": "Missing queries"}), 400

    results_dict = {}

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
                    "_id": 0,  # Ẩn ID để tránh lỗi trùng
                    "Tên lớp học phần": 1,
                    "Giảng viên": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        results = list(collection.aggregate(pipeline))

        # 🔥 Loại bỏ bản ghi trùng lặp dựa trên "Tên lớp học phần"
        unique_results = []
        seen_courses = set()
        for item in results:
            if item["Tên lớp học phần"] not in seen_courses:
                seen_courses.add(item["Tên lớp học phần"])
                unique_results.append(item)

        results_dict[query] = unique_results if unique_results else [{"Tên lớp học phần": "Không tìm thấy", "Giảng viên": "", "score": 0}]


    return jsonify(results_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
