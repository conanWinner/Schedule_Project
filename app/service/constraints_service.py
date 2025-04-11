import random
from deap import base, creator, tools, algorithms

from app.constant.constant_input_test import user_preferences
from app.constant.schedule_of_classes import schedule_of_classes
from app.model.Class_Info import ClassInfo

# Thiết lập NSGA-II
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


# @desc: All of basis constraints
def non_conflict_periods(selected_classes):
    # Không trùng tiết học
    conflicts = 0
    time_slots = set()
    for _, ClassInfo in selected_classes:
        for p in ClassInfo.periods:
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
    for _,  ClassInfo in selected_classes:
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
    set_preference = set(preference["value"])
    score = 0
    for _, ClassInfo in selected_classes:
        set_periods = set(ClassInfo.periods)
        same_periods = set_preference & set_periods
        num_same_periods = len(same_periods)
        score += num_same_periods

    return -score if preference['like'] else score



def teacher(selected_classes, preference):
    preferred_teachers = preference["name"]
    score = 0
    for _, ClassInfo in selected_classes:
        if ClassInfo.teacher in preferred_teachers:
            score += 1

    return -score if preference["like"] else score

def area(selected_classes, preference):
    preferred_areas = preference["value"]
    score = 0
    for _, ClassInfo in selected_classes:
        if ClassInfo.area in preferred_areas:
            score += 1

    return -score if preference["like"] else score

def room(selected_classes, preference):
    preferred_rooms = preference["value"]
    score = 0
    for _, ClassInfo in selected_classes:
        if ClassInfo.room in preferred_rooms:
            score += 1

    return -score if preference["like"] else score


def day(selected_classes, preference):
    preferred_days = preference["value"]
    score = 0
    for _, ClassInfo in selected_classes:
        if ClassInfo.day in preferred_days:
            score += 1

    return -score if preference["like"] else score

def sub_per_session(selected_classes, preference):
    required_periods = preference["value"]

    counts = [len(ClassInfo.periods) for _, ClassInfo in selected_classes]

    total_mismatch = sum(abs(required_periods - count) for count in counts)

    return total_mismatch

def sub_per_day(selected_classes, preference):
    subject_per_day = preference["value"]
    sub_counts = {}
    for _, ClassInfo in selected_classes:
        sub_counts[ClassInfo.day] = sub_counts.get(ClassInfo.day, 0) + 1

    total_missing = sum(abs(subject_per_day - count) for count in sub_counts.values())

    return total_missing


def period_onward(selected_classes, preference):
    min_period = preference["value"]
    score = sum(1 for _, ClassInfo in selected_classes if min(ClassInfo.periods) >= min_period)
    return -score if preference["like"] else score

def hour_onward(selected_classes, preference):
    def period_to_hour(period):
        start_time = schedule_of_classes.get(period - 1, None)
        if start_time:
            return start_time
        return 0  # Nếu không có thông tin, trả về giá trị mặc định

    min_hour = preference["value"]
    score = sum(
        1 for _, ClassInfo in selected_classes if
        period_to_hour(min(ClassInfo.periods)) >= min_hour
    )

    return -score if preference["like"] else score


def rest_interval(selected_classes, preference):
    gaps = 0
    day_periods = {}
    for _, ClassInfo in selected_classes:
        if ClassInfo.day not in day_periods:
            day_periods[ClassInfo.day] = []
        day_periods[ClassInfo.day].extend(ClassInfo.periods)

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

def convert_to_classinfo_dict(raw_dict):
    tiet_raw = raw_dict.get("Tiết", [])

    if isinstance(tiet_raw, str):
        try:
            periods = eval(tiet_raw)
        except:
            periods = []
    elif isinstance(tiet_raw, list):
        periods = tiet_raw
    else:
        periods = []

    return {
        "class_index": raw_dict.get("Lớp", ""),
        "language": raw_dict.get("Ngôn ngữ", ""),
        "field": raw_dict.get("Chuyên ngành", ""),
        "sub_topic": raw_dict.get("Chủ đề phụ", ""),
        "teacher": raw_dict.get("Giảng viên", ""),
        "day": raw_dict.get("Thứ", ""),
        "periods": periods,
        "area": raw_dict.get("Khu vực", ""),
        "room": raw_dict.get("Số phòng", ""),
        "class_size": raw_dict.get("Sỉ số", 0)
    }


CONSTRAINT_FUNCTIONS = {
    "periods": periods,
    "teacher": teacher,
    "area": area,
    "room": room,
    "day": day,
    "subject_per_session": sub_per_session,
    "subject_per_day": sub_per_day,
    "period_onward": period_onward,
    "hour_onward": hour_onward,
    "rest_interval": rest_interval
}

def evaluate(individual, user_preferences, USER_INPUT, COURSES):
    selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]
    # Chuyển đổi dict -> ClassInfo
    selected_classes = [(user_input, ClassInfo(**convert_to_classinfo_dict(class_dict))) for user_input, class_dict in selected_classes]

    conflict = non_conflict_periods(selected_classes)

    priority_score = 0
    for key, preference in user_preferences.items():
        if key in CONSTRAINT_FUNCTIONS:
            priority_score += CONSTRAINT_FUNCTIONS[key](selected_classes, preference)

    priority_score += conflict
    return (priority_score, )


toolbox = base.Toolbox()



def run_nsga_ii(courses_data):
    USER_INPUT = list(courses_data.keys())
    COURSE_OPTIONS = [len(courses_data[course]) for course in USER_INPUT]
    POPULATION_SIZE = 30
    CROSSOVER = 0.7
    MUTATION = 0.3
    NUMBER_OF_GEN = 50


    # Đăng ký các hàm với toolbox
    def init_individual():
        return creator.Individual([random.randint(0, options - 1) for options in COURSE_OPTIONS])

    toolbox.register("individual", init_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: evaluate(ind, user_preferences, USER_INPUT, courses_data))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=[o - 1 for o in COURSE_OPTIONS], indpb=MUTATION)
    toolbox.register("select", tools.selNSGA2)

    # Chạy thuật toán
    random.seed(42)
    pop = toolbox.population(n=POPULATION_SIZE)
    algorithms.eaMuPlusLambda(pop, toolbox, mu=POPULATION_SIZE, lambda_=POPULATION_SIZE, cxpb=CROSSOVER, mutpb=MUTATION, ngen=NUMBER_OF_GEN, verbose=False)

    # Lấy kết quả Pareto front
    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]

    # Chuẩn bị kết quả trả về
    results = []
    for ind in pareto_front:
        schedule = [(USER_INPUT[i], courses_data[USER_INPUT[i]][idx]) for i, idx in enumerate(ind)]
        results.append({
            "schedule": schedule,
            "score": abs(ind.fitness.values[0])
        })

    return results
