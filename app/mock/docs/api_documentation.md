# API Documentation

## 1. Search API

### Input:
```json
{
  "query": "du lieu" // là tên môn học/ chủ đề phụ cần được gợi ý khi search
}
```

### Output:
```json
{
  "query": "du lieu",
  "results": [
    {
      "course_name": "Phân tích dữ liệu",
      "sub_topic": "Pandas, trực quan hóa với Matplotlib"
    },
    {
      "course_name": "Cơ sở dữ liệu",
      "sub_topic": "Cơ sở dữ liệu"
    },
    {
      "course_name": "Xử lý dữ liệu",
      "sub_topic": ""
    },
    {
      "course_name": "Kho dữ liệu",
      "sub_topic": ""
    }
  ]
}
```

### Gợi ý xử lý kết quả:
- Nối `course_name @ sub_topic` để gợi ý cho người dùng chọn.
- Nếu không có `sub_topic`, chỉ dùng `course_name`.

---

## 2. Schedule API

### Input:
```json
{
  "query": [
    "Phân tích dữ liệu @ Pandas, trực quan hóa với Matplotlib",
    "Cơ sở dữ liệu @ Cơ sở dữ liệu",
    "Xử lý dữ liệu"
  ],
  "prompt": "Tôi chỉ học nếu lớp bắt đầu sau 10 giờ sáng. Tôi thích lịch học trải đều trong tuần, ..."
}
```

### Output:
```json
{
  "schedules": [
    {
      "schedule": [
        {
          "subject": "Automat và ngôn ngữ hình thức",
          "class_info": {
            "name": "Automat và ngôn ngữ hình thức",
            "class_index": "3",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "CLC_Kỹ thuật phần mềm",
            "teacher": "TS.Nguyễn Đức Hiển",
            "day": "Thứ Hai",
            "periods": [1, 2],
            "area": "K",
            "room": "A113",
            "class_size": 70
          }
        },
        {
          "subject": "Bảo mật và an toàn hệ thống thông tin",
          "class_info": {
            "name": "Bảo mật và an toàn hệ thống thông tin",
            "class_index": "2",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "VP_Công nghệ thông tin",
            "teacher": "TS.Đặng Quang Hiển",
            "day": "Thứ Hai",
            "periods": [6, 7, 8],
            "area": "V",
            "room": "A214",
            "class_size": 60
          }
        },
        {
          "subject": "Cấu trúc dữ liệu và giải thuật",
          "class_info": {
            "name": "Cấu trúc dữ liệu và giải thuật",
            "class_index": "1",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "JIT_Khoa học máy tính",
            "teacher": "ThS.Lê Song Toàn",
            "day": "Thứ Sáu",
            "periods": [1, 2],
            "area": "K",
            "room": "A101",
            "class_size": 90
          }
        }
      ],
      "score": 1.0
    },
    {
      "schedule": [
        {
          "subject": "Automat và ngôn ngữ hình thức",
          "class_info": {
            "name": "Automat và ngôn ngữ hình thức",
            "class_index": "2",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "CLC_Kỹ thuật phần mềm",
            "teacher": "ThS.Dương Thị Mai Nga",
            "day": "Thứ Tư",
            "periods": [3, 4],
            "area": "K",
            "room": "A313",
            "class_size": 75
          }
        },
        {
          "subject": "Bảo mật và an toàn hệ thống thông tin",
          "class_info": {
            "name": "Bảo mật và an toàn hệ thống thông tin",
            "class_index": "2",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "VP_Công nghệ thông tin",
            "teacher": "TS.Đặng Quang Hiển",
            "day": "Thứ Hai",
            "periods": [6, 7, 8],
            "area": "V",
            "room": "A214",
            "class_size": 60
          }
        },
        {
          "subject": "Cấu trúc dữ liệu và giải thuật",
          "class_info": {
            "name": "Cấu trúc dữ liệu và giải thuật",
            "class_index": "1",
            "language": "Tiếng Việt",
            "field": "IT",
            "sub_topic": "JIT_Khoa học máy tính",
            "teacher": "ThS.Lê Song Toàn",
            "day": "Thứ Sáu",
            "periods": [1, 2],
            "area": "K",
            "room": "A101",
            "class_size": 90
          }
        }
      ],
      "score": 0.8
    }
  ],
  "message": "Đã sắp xếp thành công"
}
```
