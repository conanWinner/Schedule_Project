import pandas as pd

# Đọc file Excel gốc
df = pd.read_excel("./output/Dataset_Cleaned_Nguyen.xlsx")  # thay bằng tên file của bạn


if 'Số phòng' in df.columns:
    # Lấy cột Giảng Viên và loại bỏ giá trị trùng lặp, NaN
    unique_lecturers = df['Số phòng'].dropna().drop_duplicates()

    # Chuyển sang DataFrame mới
    new_df = pd.DataFrame(unique_lecturers, columns=['Số phòng'])

    # Ghi vào file mới
    new_df.to_excel("./output/phong_khong_trung_lap.xlsx", index=False)

    print("✅ Đã lưu danh sách số phòng không trùng lặp vào 'phong_khong_trung_lap.xlsx'")
else:
    print("❌ Không tìm thấy cột 'Số phòng' trong file Excel.")
