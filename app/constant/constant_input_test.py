# Dữ liệu mẫu (danh sách lớp học)
from sympy import true, false
from sympy.parsing.sympy_parser import null

from app.model.Class_Info import ClassInfo


COURSES = {
    "Automat và ngôn ngữ hình thức": [
        ClassInfo("Automat và ngôn ngữ hình thức", "1", "Tiếng Việt", "IT", "CLC_Kỹ thuật phần mềm", "ThS.Trần Đình Sơn", "Thứ Sáu", [8, 9], "K", "A213", 80),
        ClassInfo("Automat và ngôn ngữ hình thức", "2", "Tiếng Việt", "IT", "CLC_Kỹ thuật phần mềm", "ThS.Dương Thị Mai Nga", "Thứ Tư", [3, 4], "K", "A313", 75),
        ClassInfo("Automat và ngôn ngữ hình thức", "3", "Tiếng Việt", "IT", "CLC_Kỹ thuật phần mềm", "TS.Nguyễn Đức Hiển", "Thứ Hai", [1, 2], "K", "A113", 70),
    ],
    "Bảo mật và an toàn hệ thống thông tin": [
        ClassInfo("Bảo mật và an toàn hệ thống thông tin", "1", "Tiếng Việt", "IT", "VP_Công nghệ thông tin", "ThS.Trần Thanh Liêm", "Thứ Sáu", [1, 2, 3, 4], "K", "B306",
         85),
        ClassInfo(
            "Bảo mật và an toàn hệ thống thông tin", "2", "Tiếng Việt", "IT", "VP_Công nghệ thông tin", "ThS.Trần Đình Sơn", "Thứ Hai", [6, 7, 8], "V", "A214",
            60),
    ],
    "Cấu trúc dữ liệu và giải thuật": [
        ClassInfo("Cấu trúc dữ liệu và giải thuật", "1", "Tiếng Việt", "IT", "JIT_Khoa học máy tính", "ThS.Lê Song Toàn", "Thứ Sáu", [1, 2], "K", "A101", 90),
        ClassInfo("Cấu trúc dữ liệu và giải thuật", "2", "Tiếng Việt", "IT", "JIT_Khoa học máy tính", "PGS.TS.Nguyễn Thanh Bình", "Thứ Hai", [1, 2], "K", "A110",
         95),
    ]
}

# Các môn học mà người dùng chọn
USER_INPUT = ["Automat và ngôn ngữ hình thức", "Bảo mật và an toàn hệ thống thông tin",
              "Cấu trúc dữ liệu và giải thuật"]


USER_PREFERENCES ={
    "defaults": {
        "subject_per_session": null,
        "subject_per_day": null,
        "duration_of_session": null,
        "period_onward": null,
        "hour_onward": null,
        "area": [

        ],
        "room": [
             {"value": "A101", "like": true}
        ],
        "class": [
            # {
            #     "name": "",
            #     "class_group": [],
            #     "teacher": [
            #         {"name": "ThS.Trần Đình Sơn", "like": false},
            #     ]
            # },
            # {
            #     "name": "Automat và ngôn ngữ hình thức",
            #     "class_group": [
            #         {"value":  2, "like":  false},
            #     ],
            #     "teacher": [
            #         {"name": "ThS.Dương Thị Mai Nga", "like": false},
            #     ]
            # }
        ],
        "rest_interval": null
    },
    "periods": [
        {
            "day":
                {"value": "Thứ Sáu", "like": true}
            ,
            "period":null,
            # {"value": [1, 2, 3, 4, 5, 6, 7, 8, 9], "like": true},
            "subject_count":null,
            # {"value": 1, "like": true},
            "duration_of_session": null,
            "rest_interval": null,
            "room": [],
            "area": null,
            "class": [
                {
                    "name": "",
                    "class_group": [],
                    "teacher": [
                        {"name": "ThS.Trần Đình Sơn", "like": true},
                    ]
                },
            ],
            "period_onward": null,
            "hour_onward": null
        },
    ]
}
