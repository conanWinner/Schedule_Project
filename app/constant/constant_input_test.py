
# Dữ liệu mẫu (danh sách lớp học)
COURSES = {
    "Automat và ngôn ngữ hình thức": [
        ("ThS.Trần Đình Sơn", "Thứ Sáu", [8, 9], "K", "A213"),
        ("ThS.Dương Thị Mai Nga", "Thứ Tư", [3, 4], "K", "A313"),
        ("TS.Nguyễn Đức Hiển", "Thứ Hai", [1, 2], "K", "A113"),
    ],
    "Bảo mật và an toàn hệ thống thông tin": [
        ("ThS.Trần Thanh Liêm", "Thứ Sáu", [1, 2, 3, 4], "K", "B306"),
        ("TS.Đặng Quang Hiển", "Thứ Hai", [6, 7, 8], "V", "A214"),
    ],
    "Cấu trúc dữ liệu và giải thuật": [
        ("ThS.Lê Song Toàn", "Thứ Sáu", [1, 2], "K", "A101"),
        ("PGS.TS.Nguyễn Thanh Bình", "Thứ Hai", [1, 2], "K", "A110"),
    ]
}

# Các môn học mà người dùng chọn
USER_INPUT = ["Automat và ngôn ngữ hình thức", "Bảo mật và an toàn hệ thống thông tin",
              "Cấu trúc dữ liệu và giải thuật"]


user_preferences = {
    "periods": {"value": [1, 2, 3, 4], "like": True},
    "teacher": {"name": ["ThS.Dương Thị Mai Nga", "TS.Nguyễn Đức Hiển"], "like": False},
    # "room": {"room": "A.101", "like": True},
    # "period_onward": {"period_onward": 6, "like": False}
}