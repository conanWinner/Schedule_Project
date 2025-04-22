import pandas as pd
from dotenv import load_dotenv
from app.config.database_configuration import get_database
from app.config.embedding_model import load_model

# Tải các biến môi trường từ file ..env
load_dotenv()

# Kết nối tới MongoDB
db = get_database()
collection = db["ly_courses"]

# Load model Sentence Transformers
model = load_model()

# Đọc dữ liệu từ file Excel đã chuẩn hóa
df = pd.read_excel("../../data/input/Final_Dataset.xlsx")

# Đổi tên cột sang tiếng Anh để đồng bộ với ClassInfo
column_mapping = {
    "Tên học phần": "course_name",
    "Lớp": "class_index",
    "Ngôn ngữ": "language",
    "Chuyên ngành": "field",
    "Chủ đề phụ": "sub_topic",
    "Giảng viên": "teacher",
    "Thứ": "day",
    "Tiết": "periods",
    "Khu vực": "area",
    "Số phòng": "room",
    "Sỉ số": "class_size"
}
df.rename(columns=column_mapping, inplace=True)

# Tạo list dữ liệu có embedding
data = []
for _, row in df.iterrows():
    course_name = row.get("course_name", "")
    sub_topic = row.get("sub_topic", "")

    if course_name and sub_topic:
        combined_text = f"{course_name} - {sub_topic}"
    elif course_name:
        combined_text = course_name
    else:
        combined_text = ""

    if combined_text:
        embedding = model.encode(combined_text).tolist()
    else:
        embedding = []

    row_dict = row.to_dict()

    # Chuyển periods nếu cần (chuỗi sang list)
    if isinstance(row_dict.get("periods"), str):
        try:
            row_dict["periods"] = eval(row_dict["periods"])
        except:
            row_dict["periods"] = []

    row_dict["embedding"] = embedding
    data.append(row_dict)

# Xóa dữ liệu cũ (nếu cần)
collection.delete_many({})

# Chèn vào MongoDB
collection.insert_many(data)
print("✅ Đã import dữ liệu + embedding với tên field tiếng Anh!")
