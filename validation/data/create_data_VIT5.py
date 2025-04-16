import pandas as pd
import random

# Danh sách các dấu nối thường gặp
connectors = [", ", " ", ". ", " và ", " hoặc "]

# Đọc dữ liệu từ file Excel
df = pd.read_excel("../../data/input/Pre-Input_for_VIT5.xlsx")  # Đổi tên nếu cần
df = df.dropna(subset=["Prompt", "Type"])  # Bỏ dòng trống nếu có

# Danh sách tất cả các loại type (có thể mở rộng thêm nếu cần)
all_types = df['Type'].unique().tolist()

# Lấy toàn bộ danh sách prompt
all_prompts = df['Prompt'].tolist()

# Danh sách kết quả cuối cùng
result = []

NUM_OF_CONSTRAINT = 11

# Duyệt qua từng loại type
for t in all_types:
    # Lấy các prompt thuộc type hiện tại
    starting_prompts = df[df['Type'] == t]['Prompt'].sample(len(df[df['Type'] == t]))

    for start_prompt in starting_prompts:
        for n in range(1, 8):  # Ghép từ 1 đến 8 câu
            sampled_prompts = random.sample(
                [p for p in all_prompts if p != start_prompt],  # Tránh lặp lại chính nó
                min(n, len(all_prompts) - 1)
            )

            # Tạo chuỗi với các connector ngẫu nhiên
            joined_prompts = ''
            for i, p in enumerate(sampled_prompts):
                connector = random.choice(connectors)
                joined_prompts += p
                if i < len(sampled_prompts) - 1:
                    joined_prompts += connector

            connector = random.choice(connectors)
            final = f"{start_prompt}{connector}{joined_prompts}"
            result.append(final)

# In kết quả
# for line in result:
#     print(line)

print(len(result))
# (Tùy chọn) Ghi ra file CSV
pd.DataFrame({'Kết quả': result}).to_excel("./output/Final_Dataset_VIT5.xlsx", index=False)
# KẾt quả cuối cùng tổng cộng: 3829 dòng