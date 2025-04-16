import pandas as pd

# Đọc file Excel
df = pd.read_excel("./output/Dataset_Cleaned_Nguyen.xlsx")

# Kiểm tra cột
if 'Tên học phần' in df.columns and 'Chủ đề phụ' in df.columns and 'Giảng viên' in df.columns:
    # Gộp 3 cột lại thành 1 chuỗi theo định dạng mong muốn
    def merge_columns(row):
        subject = str(row['Tên học phần']).strip()
        sub_topic = str(row['Chủ đề phụ']).strip() if pd.notna(row['Chủ đề phụ']) else ""
        teacher = str(row['Giảng viên']).strip()
        # Nếu có chủ đề phụ thì gộp thêm, còn không thì chỉ tên học phần
        full_subject = f"{subject} {sub_topic}".strip()
        return f"{full_subject} @ {teacher}"

    df['Gộp thông tin'] = df.apply(merge_columns, axis=1)

    # Loại bỏ trùng lặp
    df_unique = df[['Gộp thông tin']].drop_duplicates()

    # Tách lại thành 2 cột
    df_unique[['Tên học phần + Chủ đề phụ', 'Giảng viên']] = df_unique['Gộp thông tin'].str.split(' @ ', expand=True)

    # Xoá cột gộp tạm
    df_final = df_unique.drop(columns=['Gộp thông tin'])

    # Ghi ra file mới
    df_final.to_excel("./output/hoc_phan_giang_vien_khong_trung.xlsx", index=False)

    print("✅ Đã tạo file 'hoc_phan_giang_vien_khong_trung.xlsx' thành công.")
else:
    print("❌ Thiếu một trong các cột: 'Tên học phần', 'Chủ đề phụ', hoặc 'Giảng viên'.")
