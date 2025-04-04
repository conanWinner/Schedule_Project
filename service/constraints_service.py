
from utils.schedule_of_classes import schedule_of_classes

# @desc: All of basis constraints
def non_conflict_periods(selected_classes):
    # Không trùng tiết học
    conflicts = 0
    time_slots = set()
    for _, (teacher, day, periods, area, room) in selected_classes:
        for p in periods:
            slot = (day, p)
            if slot in time_slots:
                conflicts += 1
            time_slots.add(slot)

    return conflicts

def check_number_of_student(selected_classes):
    return

# @desc: Optional constraint
def min_gap_between_classes(selected_classes):
    # khoảng trống giữa các tiết học là nhỏ nhất
    gaps = 0
    day_periods = {}
    for _, (teacher, day, periods, area, room) in selected_classes:
        if day not in day_periods:
            day_periods[day] = []
        day_periods[day].extend(periods)

    for day in day_periods:
        periods = sorted(set(day_periods[day]))
        if len(periods) > 1:
            for i in range(len(periods) - 1):
                gaps += periods[i + 1] - periods[i] - 1

    return gaps


def periods(selected_classes, preference):
    set_preference = set(preference["value"])
    score = 0
    for _, (_, _, periods, _, _) in selected_classes:
        set_periods = set(periods)
        same_periods = set_preference & set_periods
        num_same_periods = len(same_periods)
        score += num_same_periods

    return -score if preference['like'] else score



def teacher(selected_classes, preference):
    preferred_teachers = preference["name"]
    score = 0
    for _, (teacher, _, _, _, _) in selected_classes:
        if teacher in preferred_teachers:
            score += 1

    return -score if preference["like"] else score

def area(selected_classes, preference):
    preferred_areas = preference["value"]
    score = 0
    for _, (_, _, _, area, _) in selected_classes:
        if area in preferred_areas:
            score += 1

    return -score if preference["like"] else score

def room(selected_classes, preference):
    preferred_rooms = preference["value"]
    score = 0
    for _, (_, _, _, _, room) in selected_classes:
        if room in preferred_rooms:
            score += 1

    return -score if preference["like"] else score


def day(selected_classes, preference):
    preferred_days = preference["value"]
    score = 0
    for _, (_, day, _, _, _) in selected_classes:
        if day in preferred_days:
            score += 1

    return -score if preference["like"] else score

def sub_per_session(selected_classes, preference):
    required_periods = preference["value"]

    counts = [len(periods) for _, (_, _, periods, _, _) in selected_classes]

    total_mismatch = sum(abs(required_periods - count) for count in counts)

    return total_mismatch

def sub_per_day(selected_classes, preference):
    subject_per_day = preference["value"]
    sub_counts = {}
    for _, (_, day, _, _, _) in selected_classes:
        sub_counts[day] = sub_counts.get(day, 0) + 1

    total_missing = sum(abs(subject_per_day - count) for count in sub_counts.values())

    return total_missing


def period_onward(selected_classes, preference):
    min_period = preference["value"]
    score = sum(1 for _, (_, _, periods, _, _) in selected_classes if min(periods) >= min_period)
    return -score if preference["like"] else score

def hour_onward(selected_classes, preference):
    def period_to_hour(period):
        start_time = schedule_of_classes.get(period - 1, None)
        if start_time:
            return start_time
        return 0  # Nếu không có thông tin, trả về giá trị mặc định

    min_hour = preference["value"]
    score = sum(
        1 for _, (_, _, periods, _, _) in selected_classes if
        period_to_hour(min(periods)) >= min_hour
    )

    return -score if preference["like"] else score


def rest_interval(selected_classes, preference):
    gaps = 0
    day_periods = {}
    for _, (_, day, periods, _, _) in selected_classes:
        if day not in day_periods:
            day_periods[day] = []
        day_periods[day].extend(periods)

    for day in day_periods:
        periods = sorted(set(day_periods[day]))
        for i in range(len(periods) - 1):
            gap = periods[i + 1] - periods[i]
            if preference['up_or_down'] == 'up':
                if gap >= preference['value']:
                    gaps += 1
            else:
                if gap <= preference['value']:
                    gaps += 1

    return -gaps if preference['like'] else gaps
