import pandas as pd
from dotenv import load_dotenv


from app.config.database_configuration import get_database
from app.config.embedding_model import load_model

# Tải các biến môi trường từ file .env
load_dotenv()

# Kết nối tới MongoDB
db = get_database()
collection = db["ly_courses"]

# Đọc dữ liệu từ file Excel đã chuẩn hóa
df = pd.read_excel("../../data/input/Final_Dataset.xlsx")

# Chuyển đổi DataFrame thành list of dictionaries
data = df.to_dict(orient="records")

# Xóa dữ liệu cũ (nếu muốn clear collection trước khi chèn mới)
collection.delete_many({})

# Chèn dữ liệu vào MongoDB
collection.insert_many(data)
print("✅ Dữ liệu đã nhập vào MongoDB thành công!")

# Load model Sentence Transformers
model = load_model()

# Cập nhật từng môn học với embedding tương ứng
for course in collection.find():
    course_name = course.get("Tên học phần", "")
    if course_name:
        embedding = model.encode(course_name).tolist()
        collection.update_one(
            {"_id": course["_id"]},
            {"$set": {"embedding": embedding}}
        )

print("✅ Embeddings đã được tạo và lưu vào MongoDB!")
