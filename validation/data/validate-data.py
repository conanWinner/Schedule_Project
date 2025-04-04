import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
import re
from dotenv import load_dotenv


def split_ten_lop_hoc_phan(ten_lop_hoc):
    # Tìm tất cả các cụm nằm trong dấu ngoặc ()
    matches = re.findall(r"\((.*?)\)", ten_lop_hoc)

    # Xác định lớp học phần (chứa số)
    lop_hoc_phan = ""
    the_loai = ""
    for match in matches:
        if re.search(r"\d", match):  # Nếu trong ngoặc có số thì là lớp học phần
            lop_hoc_phan = f"({match})"
        else:  # Còn lại là thể loại
            the_loai += f"({match}) "

    the_loai = the_loai.strip()  # Xóa khoảng trắng dư

    # Xác định tên học phần bằng cách loại bỏ phần lớp học phần và thể loại khỏi chuỗi gốc
    if lop_hoc_phan:
        ten_hoc_phan = ten_lop_hoc.replace(lop_hoc_phan, "").strip()
    else:
        ten_hoc_phan = ten_lop_hoc  # Nếu không có lớp học phần thì giữ nguyên tên học phần

    if the_loai:
        ten_hoc_phan = ten_hoc_phan.replace(the_loai, "").strip()  # Xóa thể loại khỏi tên học phần

    return ten_hoc_phan, lop_hoc_phan, the_loai


# Tải các biến môi trường từ file .env
load_dotenv()
# Lấy giá trị của biến môi trường
mongo_uri = os.getenv('MONGO_URI')

# Đọc dữ liệu từ Excel
file_path = "../../data/input/tkb_ai.xlsx"
df = pd.read_excel(file_path, sheet_name="Table 3")

client = MongoClient(mongo_uri)

# Chọn database và collection
db = client["university_db"]
collection = db["ly_courses"]

# Xử lý dữ liệu: Chuyển đổi theo yêu cầu
data = []

for index, row in df.iterrows():
    record = {}

    ten_lop_hoc = row["Tên lớp học phần"].strip()
    record["Tên học phần"], record["Lớp học phần"], record["Kiểu học phần"] = split_ten_lop_hoc_phan(ten_lop_hoc)

    # Giảng viên
    record["Giảng viên"] = row["Giảng viên"]

    # Tách "Thời khóa biểu" thành "Thứ" và "Tiết"
    thoi_khoa_bieu = row["Thời khóa biểu"].split("|")
    record["Thứ"] = thoi_khoa_bieu[0].strip()  # Thứ
    tiet = thoi_khoa_bieu[1].strip() if len(thoi_khoa_bieu) > 1 else ""
    record["Tiết"] = ",".join([t.strip() for t in tiet.replace("->", ",").split(",")])  # Tiết

    # Tách "Phòng học" thành Khu học và Phòng học
    phong_hoc = row["Phòng học"].split(".")
    record["Khu học"] = phong_hoc[0].strip()  # Khu học
    record["Phòng học"] = phong_hoc[1].strip() if len(phong_hoc) > 1 else ""  # Phòng học

    # Tuần học
    record["Tuần học"] = row["Tuần học"]

    # Sỉ số
    record["Sỉ số"] = row["Sỉ số"]

    data.append(record)

# Giả sử `data` đã chứa danh sách các bản ghi được chuẩn hóa
df_new = pd.DataFrame(data)

# Lưu vào file Excel
df_new.to_excel("./output/output_Ly.xlsx", index=False, engine="openpyxl")

print("Dữ liệu đã được lưu vào file output_Ly.xlsx")
# Chèn dữ liệu vào MongoDB
# collection.insert_many(data)
# print("✅ Dữ liệu đã nhập vào MongoDB thành công!")

#
# # Load model Sentence Transformers
# model = SentenceTransformer("all-MiniLM-L6-v2")
#
# # Cập nhật từng môn học với embedding tương ứng
# for course in collection.find():
#     course_name = course["Tên lớp học phần"]  # Giả sử cột này chứa tên môn học
#     embedding = model.encode(course_name).tolist()
#
#     # Cập nhật MongoDB với embedding
#     collection.update_one({"_id": course["_id"]}, {"$set": {"embedding": embedding}})
#
# print("✅ Embeddings đã được tạo và lưu vào MongoDB!")
