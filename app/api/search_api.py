from flask import Blueprint, request, jsonify, current_app
import re

search_bp = Blueprint("search", __name__)

@search_bp.route("/search-recommend", methods=["POST"])
def search_recommend():
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        query_text = data['query']

        # Regex pattern để tìm gần đúng (case-insensitive)
        pattern = re.compile(f".*{re.escape(query_text)}.*", re.IGNORECASE)

        collection = current_app.db["ly_courses"]


        query = {
            "$or": [
                {"course_name": pattern},
                {"sub_topic": pattern}
            ]
        }

        cursor = collection.find(query)

        results = []
        for doc in cursor:
            course_name = doc.get("course_name", "")
            sub_topic = doc.get("sub_topic", "")

            # Đảm bảo cả hai đều là chuỗi hợp lệ
            course_name = str(course_name) if course_name is not None else ""
            sub_topic = str(
                sub_topic) if sub_topic is not None and sub_topic == sub_topic else ""  # sub_topic == sub_topic kiểm tra NaN

            result = {
                "course_name": course_name.strip(),
                "sub_topic": sub_topic.strip()
            }
            results.append(result)

        response = {
            "query": query_text,
            "results": results
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request"}), 500
