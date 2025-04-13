import pandas as pd
import time
import json
import google.generativeai as genai

# 1. Cấu hình API key
genai.configure(api_key="AIzaSyA8G0cHkXQwOQ8V07B_k4452u5WLJYkVWs")

# 2. Khởi tạo model Gemini 1.5 Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. Đọc file Excel (chỉnh đường dẫn nếu cần)
df = pd.read_excel("./input/Final_Override_Dataset_VIT5.xlsx").head(10)

# 4. Mẫu JSON schema cần sinh
json_schema_with_comment = """{

  "defaults": {
    "subject_per_session": number,             // Số môn tối đa trong một buổi
    "subject_per_day": number,                 // Số môn tối đa trong một ngày
    "duration_of_session": {                   
      "value": number,                         // Số tiết học của môn học (ví dụ: 2)
      "up_or_down": "up" | "down",             // Giới hạn tối đa hoặc tối thiểu số tiết học
      "like": boolean
    },
    "period_onward": {
      "value": number,                         // Tiết học bắt đầu ưu tiên (ví dụ: 3)
      "like": boolean
    },
    "hour_onward": {
      "value": number,                         // Giờ bắt đầu ưu tiên (ví dụ: 9)
      "unit": "hour",
      "like": boolean
    },
    "area": {
      "value": string,                         // Khu vực học mong muốn (ví dụ: "K")
      "like": boolean
    },
    "room": [                                  // Danh sách phòng học mong muốn hoặc cần tránh
      { "value": string, "like": boolean }
    ],
    "teacher": [                               // Danh sách giáo viên muốn học hoặc tránh
      { "name": string, "like": boolean }
    ],
    "class": [                                 // Lớp học phần kèm nhóm lớp
      {
        "name": string,
        "class_group": [
          { "value": number, "like": boolean }
        ]
      }
    ],
    "rest_interval": {
      "value": number,                         // Số tiết nghỉ giữa các môn (ví dụ: 1)
      "up_or_down": "up" | "down",             // Giới hạn tối đa hoặc tối thiểu thời gian nghỉ
      "like": boolean
    }
  },
  "periods": [                                  // Các ràng buộc cụ thể theo từng ngày
    {
      "day": 
        { "value": string, "like": boolean } // Tên ngày trong tuần, ví dụ: "Thứ 2"
      ,  
      "period": { "value": [number], "like": boolean }, // Các tiết học muốn học trong ngày
      "subject_count": { "value": number, "like": boolean }, // Số môn muốn học hôm đó
      "duration_of_session": {                   
        "value": number,                         
        "up_or_down": "up" | "down",             
        "like": boolean
      },
      "rest_interval": {
        "value": number,
        "up_or_down": "up" | "down",
        "like": boolean
      },
      "teacher": [ { "name": string, "like": boolean } ],
      "room": [ { "value": string, "like": boolean } ],
      "area": { "value": string, "like": boolean },
      "class": [
        {
          "name": string,
          "class_group": [
            { "value": number, "like": boolean }
          ]
        }
      ],
      "period_onward": {
        "value": number,
        "like": boolean
      },
      "hour_onward": {
        "value": number,
        "unit": "hour",
        "like": boolean
      }
    }
  ]

}"""

# 5. Hàm chuyển câu sang JSON (đã cải tiến prompt chi tiết)
def sentence_to_json(sentence):
    retries = 3
    for attempt in range(retries):
        try:
            prompt = f"""
Hãy phân tích yêu cầu của người dùng và trả về định dạng JSON theo cấu trúc sau (đã được chú thích rõ ràng):

f"{json_schema_with_comment}\n"

Output: Điền đầy đủ thông tin theo mẫu với câu: {sentence}
Gợi ý thêm:  
- "like": true nghĩa là ưu tiên, "like": false là tránh.
- Buổi sáng: tiết 1 đến tiết 5, Buổi chiều:  tiết 6 đến tiết 9, Cả ngày: tiết 1 đến tiết 9
- Sáng: Tiết 1: 07h30, Tiết 2: 08h30, Tiết 3: 09h30, Tiết 4: 10h30, Tiết 5: 11h30, Chiều: Tiết 6: 13h00, Tiết 7: 14h00, Tiết 8: 15h00, Tiết 9: 16h00, Tiết 10: 17h00"
- Tách area và room như này: V.A201 thì trước dấu chấm là area, toàn bộ sau dấu chấm là room

Lưu ý:
- Nếu không có yêu cầu cụ thể thì không cần đưa vào `periods`, chỉ đưa vào `defaults`.
- Nếu những yêu cầu đưa vào `periods`, thì không cần đưa vào `defaults` nữa
- Nếu không có thông tin nào về  field là mảng được đề cập từ người dùng thì hãy để mảng rỗng
- Nếu không có thông tin nào về  field là object được đề cập từ người dùng thì hãy để object đó là null
            """

            response = model.generate_content(
                contents=[
                    {"role": "user", "parts": [{"text": prompt}]}
                ],
                generation_config={"temperature": 0.5}
            )

            json_str = response.text.strip()

            if json_str.startswith("```json"):
                json_str = json_str[len("```json"):].strip()
            if json_str.endswith("```"):
                json_str = json_str[:-len("```")].strip()

            return json.loads(json_str)

        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                delay = 2 ** attempt
                print(f"[!] Quá tải API - thử lại sau {delay} giây...")
                time.sleep(delay)
            else:
                print(f"[!] Lỗi không mong muốn: {e}")
                return None
    return None


# 6. Xử lý từng dòng
results = []
for i, row in df.iterrows():
    sentence = str(row[0])  # giả sử câu nằm ở cột đầu tiên
    print(f"🔹 Đang xử lý dòng {i + 1}: {sentence}")
    json_output = sentence_to_json(sentence)
    if json_output:
        results.append(json_output)
    time.sleep(1)  # Tránh vượt giới hạn gọi API

# 7. Ghi kết quả ra file
with open("./output/converted_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Đã hoàn thành chuyển đổi và lưu vào file 'converted_data.json'.")
