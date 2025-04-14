# 🎨 Gợi ý thiết kế UI/UX cho hệ thống chọn lịch học

## Mục tiêu người dùng:
1. Gõ từ khóa để tìm môn học/chủ đề phụ.
2. Nhận gợi ý chính xác định dạng `course_name @ sub_topic`.
3. Chọn 1 hoặc nhiều gợi ý.
4. Gửi thêm yêu cầu cá nhân về lịch học (optional).
5. Nhận danh sách lịch học phù hợp.

---

## Gợi ý bố cục giao diện (UI Layout)

### 1. Thanh tìm kiếm với auto-complete
```
[ Nhập môn học/chủ đề phụ ] ⌄
```
- Khi gõ: hiện danh sách gợi ý dạng:
    ```
    ✅ Phân tích dữ liệu @ Pandas, trực quan hóa với Matplotlib
    ✅ Cơ sở dữ liệu @ Cơ sở dữ liệu
    ✅ Xử lý dữ liệu
    ✅ Kho dữ liệu
    ```
- Cho phép chọn nhiều (multi-select chips hoặc checkbox).

---

### 2. Hiển thị môn học đã chọn
- Sau khi chọn: hiển thị tag/chip có thể xóa:
    ```
    [Phân tích dữ liệu @ Pandas] [Cơ sở dữ liệu @ Cơ sở dữ liệu] [✎]
    ```

---

### 3. Prompt box
- Một vùng nhập văn bản (multiline textarea) với placeholder:
    ```
    Nhập yêu cầu lịch học: VD: Tôi chỉ học sau 10h sáng, thích học trải đều...
    ```

---

### 4. Nút GỬI / XEM LỊCH
- Khi nhấn: gọi API và hiển thị danh sách lịch học phù hợp.


