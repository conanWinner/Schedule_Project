import pandas as pd
import re

from validation.utils.constant import VALID_MAJORS, INVALID_ROOM


# Đọc dữ liệu từ Excel
file_path = "../../data/input/tkb_ai.xlsx"
df = pd.read_excel(file_path, sheet_name="Table 3")

# Kiểm tra xem dữ liệu có được đọc đúng không
if df.empty:
    raise ValueError("Dữ liệu không có trong file hoặc sheet không đúng.")


# Hàm xử lý cột "Tên lớp học phần"
def process_class_name(class_name):
    if pd.isna(class_name):
        return "", "", "", "", ""

    # Kiểm tra định dạng GDTC
    gdtc_match = re.match(r'GDTC\s*(\d+)\s*(?:\((.*?)\))?\s*(?:-(\d+))?', class_name)
    if gdtc_match:
        name = f'GDTC {gdtc_match.group(1)}'
        subtopic = gdtc_match.group(2) if gdtc_match.group(2) else 'Không có'
        class_num = gdtc_match.group(3) if gdtc_match.group(3) else ''
        return name.strip(), int(class_num) if class_num else "", "Tiếng Việt", "", subtopic

    # Xác định chuyên ngành
    major_match = re.search(r"\((\w+)\)", class_name)
    major = major_match.group(1) if major_match and major_match.group(1) in VALID_MAJORS else ""

    # Xác định số thứ tự lớp
    class_number_match = re.search(r"\(([-\d]+)\)", class_name)
    class_number = int(class_number_match.group(1).lstrip("-0")) if class_number_match else ""

    # Xác định ngôn ngữ
    language = "Tiếng Anh" if "_TA" in class_name else "Tiếng Việt"

    # Tách chủ đề phụ
    subtopic_match = re.search(r"_(?!TA)(.+)", class_name)
    subtopic = subtopic_match.group(1) if subtopic_match else ""

    # Lọc tên học phần chính
    name_cleaned = re.sub(r"\(.*?\)|_.*", "", class_name).strip()

    return name_cleaned, class_number, language, major, subtopic


# Áp dụng xử lý tên lớp học phần
df[["Tên học phần", "Lớp", "Ngôn ngữ", "Chuyên ngành", "Chủ đề phụ"]] = df["Tên lớp học phần"].apply(
    lambda x: pd.Series(process_class_name(str(x)))
)


# Hàm xử lý cột "Thời khóa biểu"
def process_schedule(schedule):
    if pd.isna(schedule):
        return "", ""
    schedule = str(schedule).strip()
    day_match = re.search(r"(Thứ \w+)", schedule)
    day = day_match.group(1) if day_match else ""
    period_match = re.search(r"Tiết ([\d,->]+)", schedule)
    periods = period_match.group(1) if period_match else ""
    period_list = []
    if periods:
        try:
            for part in periods.split(","):
                if "->" in part:
                    start, end = map(int, part.split("->"))
                    period_list.extend(range(start, end + 1))
                else:
                    period_list.append(int(part))
        except ValueError:
            period_list = []
    return day, period_list


# Áp dụng xử lý thời khóa biểu
df[["Thứ", "Tiết"]] = df["Thời khóa biểu"].apply(lambda x: pd.Series(process_schedule(str(x))))


# Hàm xử lý cột "Phòng học"
def process_room(room):
    if pd.isna(room):
        return "", ""
    room = str(room).strip()
    if room in INVALID_ROOM:
        return room, ""
    room_match = re.match(r"([A-Z])\.(.+)", room)
    if room_match:
        return room_match.group(1), room_match.group(2)
    return "Khác", room


# Áp dụng xử lý phòng học
df[["Khu vực", "Số phòng"]] = df["Phòng học"].apply(lambda x: pd.Series(process_room(str(x))))

# Đảm bảo tất cả các số độc lập hiển thị dưới dạng số
df["Lớp"] = pd.to_numeric(df["Lớp"], errors='coerce').astype('Int64')  # Giữ NaN thay vì chuỗi rỗng
df["Sỉ số"] = pd.to_numeric(df["Sỉ số"], errors='coerce').astype('Int64')  # Giữ NaN thay vì chuỗi rỗng

# Lưu dữ liệu đã xử lý vào file Excel
output_file = "Dataset_Cleaned_Nguyen.xlsx"
df_cleaned = df[["Tên học phần", "Lớp", "Ngôn ngữ", "Chuyên ngành", "Chủ đề phụ",
                 "Giảng viên", "Thứ", "Tiết", "Khu vực", "Số phòng", "Tuần học", "Sỉ số"]]

# Lưu vào file Excel
df_cleaned.to_excel(f"./output/{output_file}", index=False, engine="openpyxl")
print(f"Dữ liệu đã được lưu vào file {output_file}")
