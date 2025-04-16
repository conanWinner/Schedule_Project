SCHEDULE_OF_CLASSES = {
    0: 7.5,  # Tiết 1 bắt đầu lúc 7:30 sáng
    1: 8.5,  # Tiết 2 bắt đầu lúc 8:30 sáng
    2: 9.5,  # Tiết 3 bắt đầu lúc 9:30 sáng
    3: 10.5,  # Tiết 4 bắt đầu lúc 10:30 sáng
    4: 11.5,  # Tiết 5 bắt đầu lúc 11:30 sáng
    5: 13.0,  # Tiết 6 bắt đầu lúc 13:00 chiều
    6: 14.0,  # Tiết 7 bắt đầu lúc 14:00 chiều
    7: 15.0,  # Tiết 8 bắt đầu lúc 15:00 chiều
    8: 16.0,  # Tiết 9 bắt đầu lúc 16:00 chiều
    9: 17.0,  # Tiết 10 bắt đầu lúc 17:00 chiều
}

PRIORITY_WEIGHTS = {
    "teacher": 4.0,
    "day": 3.0,
    "periods": 2.0,
    "room": 1.0,
    "area": 1.0,
    "subject_per_session": 2.0,
    "subject_per_day": 2.0,
    "subject_count": 2.0,
    "period_onward": 3.0,
    "hour_onward": 3.0,
    "rest_interval": 1.0,
    "duration_of_session": 1.0,
    "class_group": 4.0
}