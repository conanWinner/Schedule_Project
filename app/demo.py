import random
from deap import base, creator, tools, algorithms

from app.constant.constant_variable import user_preferences, PREFERENCE_FUNCTIONS, USER_INPUT, COURSES
from app.constant.schedule_of_classes import schedule_of_classes

NUM_COURSES = len(USER_INPUT)
COURSE_OPTIONS = [len(COURSES[course]) for course in USER_INPUT]  # Số lớp mỗi môn

# Thiết lập NSGA-II
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


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


def init_individual():
    # [(subject_id, (teacher, day, periods, area, room))]
    return creator.Individual([random.randint(0, options - 1) for options in COURSE_OPTIONS])




# Vì thuật toán NSGA-II tối ưu theo hướng giá trị nhỏ hơn là tốt hơn, nên:
#   - Lịch không có xung đột (conflicts = 0) được ưu tiên.
#   - Lịch có khoảng trống nhỏ (gaps nhỏ) tốt hơn. (Optional)
#   - Lịch học thỏa mãn sở thích người dùng (priority_score càng âm càng tốt) được ưu tiên hơn.
def evaluate(individual, user_preferences):
    selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]

    conflict = non_conflict_periods(selected_classes)

    priority_score = 0
    for key, preference in user_preferences.items():
        if key in PREFERENCE_FUNCTIONS:
            priority_score += PREFERENCE_FUNCTIONS[key](selected_classes, preference)

    priority_score += conflict
    return (priority_score, )


toolbox = base.Toolbox()
toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", lambda ind: evaluate(ind, user_preferences))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=[o - 1 for o in COURSE_OPTIONS], indpb=0.2)
toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(42)
    pop = toolbox.population(n=30)
    algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=100, cxpb=0.7, mutpb=0.2, ngen=50, verbose=False)

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




if __name__ == "__main__":
    main()
