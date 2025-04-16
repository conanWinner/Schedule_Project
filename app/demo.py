import random
import re
import unicodedata
from collections import defaultdict

from deap import base, creator, tools, algorithms

from app.constant.constant_input_test import USER_PREFERENCES, USER_INPUT, COURSES
from app.constant.constant_of_schedule import SCHEDULE_OF_CLASSES
from app.model.Class_Info import ClassInfo

NUM_COURSES = len(USER_INPUT)
COURSE_OPTIONS = [len(COURSES[course]) for course in USER_INPUT]  # Số lớp mỗi môn

# Thiết lập NSGA-II
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


# @desc: All of basis constraints
# ClassInfo là
# print("DEBUG >>>", type(ClassInfo), ClassInfo)
# print("DEBUG >>>", type(ClassInfo[1]), ClassInfo[1])
# DEBUG >>> <class 'tuple'> ('3', 'Tiếng Việt', 'IT', 'CLC_Kỹ thuật phần mềm', 'TS.Nguyễn Đức Hiển', 'Thứ Hai', [1, 2], 'K', 'A113', 70)
# DEBUG >>> <class 'str'> Tiếng Việt
def non_conflict_periods(selected_classes):
    # Không trùng tiết học
    conflicts = 0
    time_slots = set()
    for _, ClassInfo in selected_classes:
        day = ClassInfo.day
        for p in ClassInfo.periods:
            slot = (day, p)
            if slot in time_slots:
                conflicts += 1
            time_slots.add(slot)

    return conflicts


# @desc: Optional constraint
def min_gap_between_classes(selected_classes):
    # khoảng trống giữa các tiết học là nhỏ nhất
    gaps = 0
    day_periods = {}
    for _, ClassInfo in selected_classes:
        if ClassInfo.day not in day_periods:
            day_periods[ClassInfo.day] = []
        day_periods[ClassInfo.day].extend(ClassInfo.periods)

    for day in day_periods:
        periods = sorted(set(day_periods[day]))
        if len(periods) > 1:
            for i in range(len(periods) - 1):
                gaps += periods[i + 1] - periods[i] - 1

    return gaps

def periods(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    set_preference = set(preference["value"])
    score = 0

    for _, ClassInfo in selected_classes:
        if all(p in set_preference for p in ClassInfo.periods):
            score += 1
        else:
            score += 0  # Không cộng điểm nếu có tiết nằm ngoài khoảng

    return -score * PRIORITY_WEIGHTS["periods"] if preference.get('like', False) else score


def area(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    preferred_area = preference["value"].upper()
    score = 0
    for _, ClassInfo in selected_classes:
        if ClassInfo.area == preferred_area:
            score += 1

    return -score * PRIORITY_WEIGHTS["area"] if preference.get('like', False) else score


def room(selected_classes, preference_list):
    if not preference_list:
        return 0

    score = 0
    for _, ClassInfo in selected_classes:
        for room_pref in preference_list:
            if ClassInfo.room == room_pref["value"].upper():
                if room_pref.get("like", False):
                    score += 1
                else:
                    score -= 1
                break  # Found match, no need to check other rooms

    return -score * PRIORITY_WEIGHTS["room"]



def day(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    preferred_day = normalize_day(preference["value"])
    score = 0
    for _, ClassInfo in selected_classes:
        class_day = normalize_day(ClassInfo.day)
        if class_day == preferred_day:
            score += 1

    return -score * PRIORITY_WEIGHTS["day"] if preference.get('like', False) else score


def normalize_day(day_str):
    nfkd_form = unicodedata.normalize('NFKD', day_str)
    without_diacritics = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    day_clean = without_diacritics.lower().replace(" ", "")

    # Chuẩn hóa thành dạng "thu2", "thu3", ...
    day_clean = re.sub(r"thu(?:hai|2)", "thu2", day_clean)
    day_clean = re.sub(r"thu(?:ba|3)", "thu3", day_clean)
    day_clean = re.sub(r"thu(?:tu|4)", "thu4", day_clean)
    day_clean = re.sub(r"thu(?:nam|5)", "thu5", day_clean)
    day_clean = re.sub(r"thu(?:sau|6)", "thu6", day_clean)
    day_clean = re.sub(r"thu(?:bay|7)", "thu7", day_clean)
    day_clean = re.sub(r"chunhat|chunhật|chủnhật|cn", "chunhat", day_clean)

    return day_clean

def duration_of_session(selected_classes, preference):
    """Check if the duration of sessions matches preferences"""
    if not preference or "value" not in preference:
        return 0

    required_duration = preference["value"]
    up_or_down = preference.get("up_or_down", "down")
    score = 0

    for _, ClassInfo in selected_classes:
        duration = len(ClassInfo.periods)
        if up_or_down == "up":
            if duration >= required_duration:
                score += 1
        else:  # down
            if duration <= required_duration:
                score += 1

    return -score * PRIORITY_WEIGHTS["duration_of_session"] if preference.get('like', False) else score


def subject_per_session(selected_classes, preference):
    if not preference or not isinstance(preference, int):
        return 0

    # Tạo dict lồng: sessions[day][session] = list of classes
    sessions = defaultdict(lambda: defaultdict(list))

    for _, class_info in selected_classes:
        # Xác định buổi: sáng nếu tiết đầu tiên <= 5, chiều nếu >= 6
        period_start = min(class_info.periods)
        if period_start <= 5:
            session = "morning"
        else:
            session = "afternoon"
        sessions[class_info.day][session].append(class_info)


    total_mismatch = 0
    for day in sessions:
        for session in sessions[day]:
            num_subjects = len(sessions[day][session])
            mismatch = abs(preference - num_subjects)
            total_mismatch += mismatch

    # if total_mismatch == 0:
    #     return -PRIORITY_WEIGHTS["subject_per_session"]
    # else:
        return total_mismatch * PRIORITY_WEIGHTS["subject_per_session"]


def subject_per_day(selected_classes, preference):
    if not preference or not isinstance(preference, int):
        return 0

    required_per_day = preference
    sub_counts = {}
    for _, ClassInfo in selected_classes:
        sub_counts[ClassInfo.day] = sub_counts.get(ClassInfo.day, 0) + 1

    total_missing = sum(abs(required_per_day - count) for count in sub_counts.values())

    # if total_missing == 0:
    #     return -PRIORITY_WEIGHTS["subject_per_day"]
    # else:
    return total_missing * PRIORITY_WEIGHTS["subject_per_day"]



def subject_count(selected_classes, preference):
    """
    Kiểm tra nếu số lượng môn học trong một ngày hoặc khoảng thời gian phù hợp với mong muốn

    Args:
        selected_classes: Danh sách các lớp đã chọn [(tên_môn, thông_tin_lớp),...]
        preference: Dictionary chứa giá trị mong muốn {"value": số_lượng, "like": Boolean}

    Returns:
        float: Điểm đánh giá (dương nếu ưa thích, âm nếu không ưa thích)
    """
    if not preference:
        return 0

    # Lấy giá trị và sở thích
    pref_value = preference.get("value")
    like = preference.get("like", True)

    if pref_value is None:
        return 0

    # Đếm số môn học trong mỗi ngày
    day_subjects = {}
    for subject_name, class_info in selected_classes:
        day = class_info.day
        if day not in day_subjects:
            day_subjects[day] = set()
        day_subjects[day].add(subject_name)

    # Tính điểm dựa trên sự phù hợp
    score = 0
    for day, subjects in day_subjects.items():
        num_subjects = len(subjects)

        # Thưởng/phạt dựa trên phù hợp với số lượng mong muốn
        if num_subjects == pref_value:
            score += 1



    return -score * PRIORITY_WEIGHTS["subject_count"]

def period_onward(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    min_period = preference["value"]
    score = 0
    for _, ClassInfo in selected_classes:
        if preference.get('like', True):
            if min(ClassInfo.periods) >= min_period:
                score += 1
        else:
            if min(ClassInfo.periods) < min_period:
                score += 1

    return score * PRIORITY_WEIGHTS["period_onward"]


def hour_onward(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    def period_to_hour(period, SCHEDULE_OF_CLASSES):
        start_time = SCHEDULE_OF_CLASSES.get(period - 1, None)
        if start_time:
            return start_time
        return 0

    min_hour = preference["value"]
    score = 0

    # Assuming schedule_of_classes is defined elsewhere
    for _, ClassInfo in selected_classes:
        if preference.get('like', True):
            if period_to_hour(min(ClassInfo.periods), SCHEDULE_OF_CLASSES) >= min_hour:
               score += 1
        else:
            if period_to_hour(min(ClassInfo.periods), SCHEDULE_OF_CLASSES) < min_hour:
               score += 1

    return score * PRIORITY_WEIGHTS["hour_onward"]

def rest_interval(selected_classes, preference):
    if not preference or "value" not in preference:
        return 0

    target_value = preference["value"]
    prefer_more = preference.get("up_or_down", "down") == "up"
    like = preference.get("like", False)

    day_blocks = {}
    for _, class_info in selected_classes:
        day = class_info.day
        if day not in day_blocks:
            day_blocks[day] = []
        day_blocks[day].append(class_info.periods)

    score = 0
    for day in day_blocks:
        blocks = sorted(day_blocks[day], key=lambda p: min(p))
        for i in range(len(blocks) - 1):
            end_prev = max(blocks[i])
            start_next = min(blocks[i + 1])
            gap = start_next - end_prev - 1
            if (prefer_more and gap >= target_value) or (not prefer_more and gap <= target_value):
                score += 1

    return -score * PRIORITY_WEIGHTS["rest_interval"] if like else score



# def class_name(selected_classes, class_preferences):
#     if not class_preferences:
#         return 0
#
#     score = 0
#     for _, class_info in selected_classes:
#         for class_pref in class_preferences:
#             # Kiểm tra tên lớp trống hoặc khớp với name (tên học phần)
#             pref_name = class_pref.get("name", "")
#             if not pref_name or pref_name == "" or pref_name == class_info.name:
#
#                 # Kiểm tra class_group (class_index)
#                 if "class_group" in class_pref and class_pref["class_group"]:
#                     for group_pref in class_pref["class_group"]:
#                         pref_group = group_pref.get("value")
#                         # So sánh với class_index trong class_info
#                         if pref_group is not None and str(pref_group) == class_info.class_index:
#                             if group_pref.get("like", True):
#                                 score += 1
#                             else:
#                                 score -= 1
#
#                 # Kiểm tra ưu tiên giáo viên
#                 if "teacher" in class_pref and class_pref["teacher"]:
#                     for teacher_pref in class_pref["teacher"]:
#                         pref_teacher = teacher_pref.get("name", "")
#                         if fuzzy_name_match(pref_teacher, class_info.teacher):
#                             if teacher_pref.get("like", True):
#                                 score += 1
#                             else:
#                                 score -= 1
#
#     return -score * PRIORITY_WEIGHTS["class_group"]

def class_name(selected_classes, class_preferences):
    if not class_preferences:
        return 0

    class_group_score = 0
    teacher_score = 0

    for subject, class_info in selected_classes:
        for class_pref in class_preferences:
            pref_name = class_pref.get("name", "")

            # Apply if preference has no name or matches this subject
            if not pref_name or pref_name == "" or pref_name == subject:

                # Process class group preferences
                if "class_group" in class_pref and class_pref["class_group"]:
                    for group_pref in class_pref["class_group"]:
                        pref_group = group_pref.get("value")
                        if pref_group is not None and str(pref_group) == class_info.class_index:
                            adj = 1 if group_pref.get("like", False) else -1
                            class_group_score += adj

                # Process teacher preferences
                if "teacher" in class_pref and class_pref["teacher"]:
                    for teacher_pref in class_pref["teacher"]:
                        pref_teacher = teacher_pref.get("name", "")

                        if fuzzy_name_match(pref_teacher, class_info.teacher):
                            adj = 1 if teacher_pref.get("like", False) else -1
                            teacher_score += adj

    # Apply separate weights for different preference types
    final_score = (-class_group_score * PRIORITY_WEIGHTS["class_group"]) + (
                -teacher_score * PRIORITY_WEIGHTS["teacher"])
    return final_score


def fuzzy_name_match(preference_name, actual_name):
    """
    Thực hiện so khớp linh hoạt với tên để xử lý các biến thể như chức danh, viết tắt, v.v.
    Trả về True nếu tên được coi là khớp, False ngược lại.
    """
    if not preference_name or not actual_name:
        return False

    # Chuyển cả hai tên sang chữ thường để so khớp không phân biệt chữ hoa chữ thường
    pref_lower = preference_name.lower()
    actual_lower = actual_name.lower()

    # Trường hợp khớp trực tiếp
    if pref_lower == actual_lower:
        return True

    # Kiểm tra nếu tên ưu tiên nằm trong tên thực tế
    if pref_lower in actual_lower:
        return True

    # Tách tên thành các phần để so khớp linh hoạt hơn
    pref_parts = pref_lower.split()
    actual_parts = actual_lower.split()

    # Kiểm tra nếu tên cuối cùng khớp (thường là họ)
    if pref_parts and actual_parts and pref_parts[-1] == actual_parts[-1]:
        return True

    # Kiểm tra nếu ít nhất 50% phần tên khớp
    matching_parts = sum(1 for part in pref_parts if part in actual_parts)
    if pref_parts and matching_parts / len(pref_parts) >= 0.5:
        return True

    # Xử lý các chức danh và viết tắt
    titles = ["ths.", "ts.", "gs.", "pgsts.", "pgs.ts.", "cô", "thầy"]

    # Loại bỏ chức danh khỏi tên thực tế để so sánh
    cleaned_actual = actual_lower
    for title in titles:
        cleaned_actual = cleaned_actual.replace(title, "").strip()

    # Kiểm tra lại với các chức danh đã được loại bỏ
    if pref_lower in cleaned_actual:
        return True

    # Kiểm tra tên họ với các chức danh đã loại bỏ
    cleaned_actual_parts = cleaned_actual.split()
    if pref_parts and cleaned_actual_parts:
        # Kiểm tra nếu họ khớp (phần cuối)
        if pref_parts[-1] == cleaned_actual_parts[-1]:
            return True
        # Kiểm tra nếu tên khớp (phần đầu)
        if pref_parts[0] == cleaned_actual_parts[0]:
            return True

    return False


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

# Define all constraint functions
CONSTRAINT_FUNCTIONS = {
    "period": periods,
    "area": area,
    "room": room,
    "day": day,
    "subject_per_session": subject_per_session,
    "subject_per_day": subject_per_day,
    "period_onward": period_onward,
    "hour_onward": hour_onward,
    "rest_interval": rest_interval,
    "duration_of_session": duration_of_session,
    "class": class_name  # Note: Use "class" as the key to match the JSON structure/
}


def init_individual():
    # [(subject_id, (teacher, day, periods, area, room))]
    return creator.Individual([random.randint(0, options - 1) for options in COURSE_OPTIONS])


# Vì thuật toán NSGA-II tối ưu theo hướng giá trị nhỏ hơn là tốt hơn, nên:
#   - Lịch không có xung đột (conflicts = 0) được ưu tiên.
#   - Lịch có khoảng trống nhỏ (gaps nhỏ) tốt hơn. (Optional)
#   - Lịch học thỏa mãn sở thích người dùng (priority_score càng âm càng tốt) được ưu tiên hơn.
# def evaluate(individual, USER_PREFERENCES, USER_INPUT, COURSES):
#     selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]
#
#     # Handle hard constraints
#     conflict = non_conflict_periods(selected_classes)
#     if conflict > 0:
#         return (float('inf'),)  # Invalid schedule due to conflicts
#
#     total_score = 0
#     is_full_week = False
#
#     # Track which constraints have been applied to which classes
#     # processed_constraints = []
#     processed_constraints = {(ui, ci.day): set() for ui, ci in selected_classes}
#
#     # First process specific period overrides
#     for period_pref in USER_PREFERENCES.get("periods", []):
#         day_info = period_pref.get("day", {})
#         day_value = day_info.get("value") if day_info else None
#         is_full_week = False # reset is_full_week
#
#         # If day_value is null or "Cả tuần", apply to all days of the week
#         if day_value is None or day_value == "Cả tuần":
#             day_classes = selected_classes  # Apply to all classes
#             is_full_week = True
#         else:
#             # Apply to classes on the specific day
#             day_classes = [(ui, ci) for ui, ci in selected_classes if ci.day == day_value]
#
#         if not day_classes:
#             continue
#
#
#         # Apply specific constraints for this period
#         for key, preference in period_pref.items():
#             if key in CONSTRAINT_FUNCTIONS and preference is not None and key != "day":
#                 # if is_full_week is True:
#                 #     total_score += CONSTRAINT_FUNCTIONS[key](day_classes, preference)
#                 # else:
#                     # Apply higher weight for periods
#                     total_score += CONSTRAINT_FUNCTIONS[key](day_classes, preference) * 2
#                     # Mark these constraints as processed for these classes
#                     # processed_constraints.extend(day_classes)
#                     for ui, ci in day_classes:
#                         processed_constraints[(ui, ci.day)].add(key)
#
#     # Then process defaults for constraints that haven't been applied yet
#     defaults = USER_PREFERENCES.get("defaults", {})
#     for key, preference in defaults.items():
#         if key in CONSTRAINT_FUNCTIONS:
#             # Only apply default constraints to classes that don't have a specific period override
#             unprocessed_classes = []
#             # if is_full_week is True:
#             #     for ui, ci in selected_classes:
#             #         unprocessed_classes.append((ui, ci))
#             # else:
#             #     for ui, ci in selected_classes:
#             #         if (ui, ci) not in processed_constraints:
#             #             unprocessed_classes.append((ui, ci))
#
#             for ui, ci in selected_classes:
#                 if key not in processed_constraints[(ui, ci.day)]:
#                     unprocessed_classes.append((ui, ci))
#
#             if unprocessed_classes:
#                 total_score += CONSTRAINT_FUNCTIONS[key](unprocessed_classes, preference)
#
#     return (total_score,)

# def evaluate(individual, USER_PREFERENCES, USER_INPUT, COURSES):
#     selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]
#
#     # Debug output
#     print("\n=== EVALUATING SCHEDULE ===")
#     print("Selected classes:")
#     for subject, class_info in selected_classes:
#         print(
#             f"  {subject} - {class_info.class_index} - {class_info.teacher} - {class_info.day} - Periods: {class_info.periods}")
#
#     # Handle hard constraints
#     conflict = non_conflict_periods(selected_classes)
#     if conflict > 0:
#         print(f"INVALID SCHEDULE: {conflict} conflicts detected")
#         return (float('inf'),)  # Invalid schedule due to conflicts
#
#     total_score = 0
#     processed_constraints = {(ui, ci.day): set() for ui, ci in selected_classes}
#
#     # Process default constraints first for better debugging
#     print("\nProcessing default constraints:")
#     defaults = USER_PREFERENCES.get("defaults", {})
#     for key, preference in defaults.items():
#         if key in CONSTRAINT_FUNCTIONS and preference is not None:
#             print(f"  Applying default constraint: {key}")
#             constraint_score = CONSTRAINT_FUNCTIONS[key](selected_classes, preference)
#             total_score += constraint_score
#             print(f"    Score contribution: {constraint_score}")
#
#             # Mark these constraints as processed
#             for ui, ci in selected_classes:
#                 processed_constraints[(ui, ci.day)].add(key)
#
#     # Then process specific period overrides
#     print("\nProcessing period-specific constraints:")
#     for i, period_pref in enumerate(USER_PREFERENCES.get("periods", [])):
#         print(f"  Period preference #{i + 1}:")
#         day_info = period_pref.get("day", {})
#         day_value = day_info.get("value") if day_info else None
#
#         print(f"    Day: {day_value or 'All days'}")
#
#         # If day_value is null or "Cả tuần", apply to all days of the week
#         if day_value is None or day_value == "Cả tuần":
#             day_classes = selected_classes  # Apply to all classes
#         else:
#             day_classes = [(ui, ci) for ui, ci in selected_classes if ci.day == day_value]
#
#         if not day_classes:
#             print("    No matching classes for this day")
#             continue
#
#         # Apply specific constraints for this period
#         for key, preference in period_pref.items():
#             if key in CONSTRAINT_FUNCTIONS and preference is not None and key != "day":
#                 print(f"    Applying constraint: {key}")
#                 # Apply higher weight for periods
#                 constraint_score = CONSTRAINT_FUNCTIONS[key](day_classes, preference) * 2
#                 total_score += constraint_score
#                 print(f"      Score contribution: {constraint_score}")
#
#                 # Mark these constraints as processed
#                 for ui, ci in day_classes:
#                     processed_constraints[(ui, ci.day)].add(key)
#
#     print(f"\nTotal fitness score: {total_score}")
#     return (total_score,)

def evaluate(individual, USER_PREFERENCES, USER_INPUT, COURSES):
    selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]

    # Debug output
    print("\n=== EVALUATING SCHEDULE ===")
    print("Selected classes:")
    for subject, class_info in selected_classes:
        print(
            f"  {subject} - {class_info.class_index} - {class_info.teacher} - {class_info.day} - Periods: {class_info.periods}")

    # Handle hard constraints
    conflict = non_conflict_periods(selected_classes)
    if conflict > 0:
        print(f"INVALID SCHEDULE: {conflict} conflicts detected")
        return (float('inf'),)  # Invalid schedule due to conflicts

    total_score = 0

    # Initialize tracking for processed constraints
    # Each key is a (subject, day) tuple, and the value is a set of constraint types already processed
    processed_constraints = {(ui, ci.day): set() for ui, ci in selected_classes}

    # First process specific period overrides - they take precedence
    print("\nProcessing period-specific constraints:")
    for i, period_pref in enumerate(USER_PREFERENCES.get("periods", [])):
        print(f"  Period preference #{i + 1}:")
        day_info = period_pref.get("day", {})
        day_value = day_info.get("value") if day_info else None

        print(f"    Day: {day_value or 'All days'}")

        # If day_value is null or "Cả tuần", apply to all days of the week
        if day_value is None or day_value == "Cả tuần":
            day_classes = selected_classes  # Apply to all classes
        else:
            day_classes = [(ui, ci) for ui, ci in selected_classes if ci.day == day_value]

        if not day_classes:
            print("    No matching classes for this day")
            continue

        # Apply specific constraints for this period
        for key, preference in period_pref.items():
            if key in CONSTRAINT_FUNCTIONS and preference is not None and key != "day":
                print(f"    Applying period-specific constraint: {key}")
                # Apply higher weight for periods
                constraint_score = CONSTRAINT_FUNCTIONS[key](day_classes, preference) * 2
                total_score += constraint_score
                print(f"      Score contribution: {constraint_score}")
                # Kiểm tra xem giá trị của preference có phải là None hoặc mảng rỗng không
                if preference is None or (isinstance(preference, list) and len(preference) == 0):
                    # Nếu preference là None hoặc mảng rỗng, không làm gì cả
                    pass
                else:
                    # Nếu preference không phải là None hoặc mảng rỗng,
                    # đánh dấu các ràng buộc đã xử lý cho các lớp/ngày cụ thể này
                    # Mark these constraints as processed for these specific class/day combinations
                    for ui, ci in day_classes:
                        processed_constraints[(ui, ci.day)].add(key)





    # Then process defaults for constraints that haven't been applied yet
    print("\nProcessing default constraints:")
    defaults = USER_PREFERENCES.get("defaults", {})
    for key, preference in defaults.items():
        if key in CONSTRAINT_FUNCTIONS and preference is not None:
            # Only apply default constraints to classes that don't have a specific period override
            # for this constraint type
            unprocessed_classes = []
            for ui, ci in selected_classes:
                if key not in processed_constraints[(ui, ci.day)]:
                    unprocessed_classes.append((ui, ci))

            if unprocessed_classes:
                print(f"Applying default constraint '{key}' to {len(unprocessed_classes)} unprocessed classes: {unprocessed_classes}")
                constraint_score = CONSTRAINT_FUNCTIONS[key](unprocessed_classes, preference)
                total_score += constraint_score
                print(f"    Score contribution: {constraint_score}")
            else:
                print(f"  Skipping default constraint '{key}' - all classes already processed")

    print(f"\nTotal fitness score: {total_score}")

    return (total_score,)


toolbox = base.Toolbox()
toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", lambda ind: evaluate(ind, USER_PREFERENCES, USER_INPUT, COURSES))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=[o - 1 for o in COURSE_OPTIONS], indpb=0.5)
toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(42)
    pop = toolbox.population(n=30)

    # Tham số:
    # pop: Đây là quần thể (population) ban đầu. pop là một danh sách các cá thể (individuals) mà thuật toán tiến hoá sẽ làm việc với. Trong trường hợp của bạn, pop được khởi tạo từ toolbox.population(n=30) với 30 cá thể.
    #
    # toolbox: Đây là đối tượng chứa các công cụ và chiến lược của thuật toán tiến hoá, bao gồm các hàm tạo cá thể, hàm đánh giá, hàm lai ghép (crossover), hàm đột biến (mutation), và hàm chọn lọc (selection).
    #
    # mu (Số lượng cá thể mẹ): mu là số lượng cá thể trong quần thể mẹ (mà thuật toán tiến hoá sẽ tạo ra qua các thế hệ). Ở đây, mu=100 có nghĩa là sẽ có 100 cá thể trong quần thể mẹ.
    #
    # lambda_ (Số lượng cá thể con): lambda_ là số lượng cá thể con được sinh ra trong mỗi thế hệ mới. Ở đây, lambda_=100, có nghĩa là 100 cá thể con sẽ được sinh ra trong mỗi thế hệ.
    #
    # cxpb (Xác suất lai ghép): cxpb là xác suất lai ghép (crossover probability) giữa hai cá thể cha mẹ để tạo ra cá thể con. Ở đây, cxpb=0.7, có nghĩa là mỗi lần lai ghép giữa hai cá thể cha mẹ, xác suất thành công là 70%.
    #
    # mutpb (Xác suất đột biến): mutpb là xác suất đột biến (mutation probability) của một cá thể. Ở đây, mutpb=0.2, có nghĩa là 20% cá thể sẽ bị đột biến sau mỗi thế hệ.
    #
    # ngen (Số thế hệ): ngen là số thế hệ (generations) mà thuật toán sẽ chạy. Mỗi thế hệ sẽ bao gồm việc tạo ra cá thể con từ quần thể mẹ thông qua các phép lai ghép và đột biến. Ở đây, ngen=50 có nghĩa là thuật toán sẽ chạy trong 50 thế hệ.
    #
    # verbose: Tham số này quyết định mức độ chi tiết của các thông báo trong quá trình chạy. Nếu verbose=True, thuật toán sẽ in ra nhiều thông tin chi tiết về quá trình tiến hoá. Nếu verbose=False, thuật toán sẽ chạy mà không in ra nhiều thông tin.
    algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=100, cxpb=0.5, mutpb=0.5, ngen=50, verbose=False)

    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    print(pareto_front)
    print("\n🔹 Các lịch trình tối ưu:")

    for ind in pareto_front:
        schedule = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(ind)]
        print(f"📌 Lịch: {schedule}")
        print(f"❌ Số điểm ưu tiên: {ind.fitness.values[0]}")
        # print(f"🕐 Khoảng trống: {ind.fitness.values[1]}")
        # print(f"🚫 Giáo viên bị cấm: {ind.fitness.values[2]}")
        # print(f"🏠 Phòng bị cấm: {ind.fitness.values[3]}")
        # print(f"📅 Ngày bị cấm: {ind.fitness.values[4]}\n")


def test_main():
    random.seed(42)

    # Create a small population for testing
    pop = toolbox.population(n=10)

    print("=== INITIAL POPULATION ===")
    for i, ind in enumerate(pop):
        print(f"Individual {i}: {ind}")
        fitness = evaluate(ind, USER_PREFERENCES, USER_INPUT, COURSES)
        print(f"Fitness: {fitness}")

    # Run a few generations
    print("\n=== RUNNING EVOLUTION ===")
    algorithms.eaMuPlusLambda(pop, toolbox, mu=10, lambda_=10, cxpb=0.5, mutpb=0.5, ngen=5, verbose=True)

    # Show final population
    print("\n=== FINAL POPULATION ===")
    for i, ind in enumerate(pop):
        print(f"Individual {i}: {ind}")
        fitness = evaluate(ind, USER_PREFERENCES, USER_INPUT, COURSES)
        print(f"Fitness: {fitness}")

    # Show best schedule
    best_ind = tools.selBest(pop, 1)[0]
    print("\n=== BEST SCHEDULE ===")
    selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(best_ind)]
    for subject, class_info in selected_classes:
        print(
            f"{subject} - {class_info.class_index} - {class_info.teacher} - {class_info.day} - Periods: {class_info.periods}")


if __name__ == "__main__":
    main()
    # test_main()