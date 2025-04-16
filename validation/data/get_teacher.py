import pandas as pd

# Đọc file Excel gốc
df = pd.read_excel("./output/Dataset_Cleaned_Nguyen.xlsx")  # thay bằng tên file của bạn

# Kiểm tra xem cột 'Giảng Viên' có tồn tại không
if 'Giảng viên' in df.columns:
    # Lấy cột Giảng Viên và loại bỏ giá trị trùng lặp, NaN
    unique_lecturers = df['Giảng viên'].dropna().drop_duplicates()

    # Chuyển sang DataFrame mới
    new_df = pd.DataFrame(unique_lecturers, columns=['Giảng viên'])

    # Ghi vào file mới
    new_df.to_excel("./output/giang_vien_khong_trung_lap.xlsx", index=False)

    print("✅ Đã lưu danh sách giảng viên không trùng lặp vào 'giang_vien_khong_trung_lap.xlsx'")
else:
    print("❌ Không tìm thấy cột 'Giảng Viên' trong file Excel.")
