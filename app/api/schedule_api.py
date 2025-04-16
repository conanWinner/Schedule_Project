from collections import defaultdict
from typing import Dict, List

from flask import Blueprint, request, jsonify, current_app

from app.model.Class_Info import ClassInfo
from app.service.constraints_service import run_nsga_ii

schedule_bp = Blueprint("schedule", __name__)


#
# @schedule_bp.route("/schedule", methods=["POST"])
# def schedule():
#     data = request.json
#     queries = data.get("queries", [])
#     top_k = data.get("top_k", 20)
#
#     if not queries:
#         return jsonify({"error": "Missing queries"}), 400
#
#     collection = current_app.db["ly_courses"]
#     model = current_app.model
#
#     courses_data = {}
#
#     for query in queries:
#         query_vector = model.encode(query).tolist()
#
#         pipeline = [
#             {
#                 "$vectorSearch": {
#                     "index": "vector_index",
#                     "path": "embedding",
#                     "queryVector": query_vector,
#                     "numCandidates": 1000,
#                     "limit": top_k
#                 }
#             },
#             {"$unset": "embedding"},
#             {"$project": {...}}
#         ]
#
#         results = list(collection.aggregate(pipeline))
#
#         formatted_results = []
#         for item in results:
#             tiets = eval(item["Tiết"]) if isinstance(item["Tiết"], str) else item["Tiết"]
#             course_info = {...}  # giống như trước
#             formatted_results.append(course_info)
#
#         courses_data[query] = formatted_results or [("Không tìm thấy", "", "", "", "", "", "", [], "", "", "")]
#
#     schedules = run_nsga_ii(courses_data)
#
#     return jsonify({"schedules": schedules, "message": "Đã sắp xếp thành công"})
def parse_query_string(query_str):

    if "@" in query_str:
        course_name, sub_topic = query_str.split("@", 1)
        return course_name.strip(), sub_topic.strip()
    return query_str.strip(), None


@schedule_bp.route("/schedule", methods=["POST"])
def schedule():
    data = request.json
    queries = data.get("queries", [])
    prompt = data.get("prompt", {})

    if not queries:
        return jsonify({"error": "Missing queries"}), 400
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    collection = current_app.db["ly_courses"]

    courses_data: Dict[str, List[ClassInfo]] = defaultdict(list)

    for query in queries:
        course_name, sub_topic = parse_query_string(query)

        search_criteria = {
            "$and": []
        }
        if course_name:
            search_criteria["$and"].append({"course_name": course_name})
        if sub_topic:
            search_criteria["$and"].append({"sub_topic": sub_topic})
        matching_classes = list(collection.find(search_criteria))


        print(f"Found {len(matching_classes)} matching classes for: {search_criteria}")
        for doc in matching_classes:
            class_info = ClassInfo(
                course_name=doc.get("course_name", ""),
                class_index=doc.get("class_index", ""),
                language=doc.get("language", ""),
                field=doc.get("field", ""),
                sub_topic=doc.get("sub_topic", ""),
                teacher=doc.get("teacher", ""),
                day=doc.get("day", ""),
                periods=doc.get("periods", []),
                area=doc.get("area", ""),
                room=doc.get("room", ""),
                class_size=doc.get("class_size", 0)
            )

            courses_data[course_name].append(class_info)

    # Gọi hàm NSGA-II (bạn đã định nghĩa ở nơi khác)
    schedules = run_nsga_ii(courses_data, prompt)

    return jsonify({
        "schedules": schedules,
        "message": "Đã sắp xếp thành công"
    })
