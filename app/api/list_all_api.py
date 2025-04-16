from flask import Blueprint, jsonify, current_app

list_all_bp = Blueprint("list_all", __name__)

@list_all_bp.route("/list-all", methods=["GET"])
def list_all():
    """Endpoint để liệt kê tất cả document trong collection (dùng cho debug)"""
    try:
        collection = current_app.db["ly_courses"]
        all_docs = list(collection.find())
        result = []

        for doc in all_docs:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId -> string
            for key, value in doc.items():
                if hasattr(value, 'tolist'):  # Nếu là numpy array
                    doc[key] = value.tolist()
            result.append(doc)

        return jsonify({"count": len(result), "documents": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


