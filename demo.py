import random
from deap import base, creator, tools, algorithms

# Dữ liệu mẫu (danh sách lớp học)
COURSES = {
    "Automat và ngôn ngữ hình thức": [
        ("ThS.Trần Đình Sơn", "Thứ Sáu", [8, 9], "K.A213"),
        ("ThS.Dương Thị Mai Nga", "Thứ Tư", [3, 4], "K.A313") ,
        ("TS.Nguyễn Đức Hiển", "Thứ Hai", [1, 2], "K.A113"),
    ],
    "Bảo mật và an toàn hệ thống thông tin": [
        ("ThS.Trần Thanh Liêm", "Thứ Sáu", [1, 2, 3, 4], "K.B306"),
        ("TS.Đặng Quang Hiển", "Thứ Hai", [6, 7, 8], "V.A214"),
    ],
    "Cấu trúc dữ liệu và giải thuật": [
        ("ThS.Lê Song Toàn", "Thứ Sáu", [1, 2], "K.A101"),
        ("PGS.TS.Nguyễn Thanh Bình", "Thứ Hai", [1, 2], "K.A110"),
    ]
}

# [1, 0, 1],
# [1, 0, 1],
# [1, 0, 1],
# [1, 0, 1],

# Các môn học mà người dùng chọn
USER_INPUT = ["Automat và ngôn ngữ hình thức", "Bảo mật và an toàn hệ thống thông tin",
              "Cấu trúc dữ liệu và giải thuật"]
NUM_COURSES = len(USER_INPUT)
COURSE_OPTIONS = [len(COURSES[course]) for course in USER_INPUT]  # Số lớp mỗi môn

# Danh sách giáo viên, phòng và ngày không muốn học
UNWANTED_TEACHERS = {"ThS.Trần Thanh Liêm"}
UNWANTED_ROOMS = {"K.A213", "V.A214"}
UNWANTED_DAYS = {"Thứ Hai", "Thứ Sáu"}

# Thiết lập NSGA-II
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)


def init_individual():
    return creator.Individual([random.randint(0, options - 1) for options in COURSE_OPTIONS])


def evaluate(individual):
    selected_classes = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(individual)]

    # Không trùng tiết học
    conflicts = 0
    time_slots = set()
    for _, (teacher, day, periods, room) in selected_classes:
        for p in periods:
            slot = (day, p)
            if slot in time_slots:
                conflicts += 1
            time_slots.add(slot)

    # khoảng trống giữa các tiết học laf nhỏ nhất
    gaps = 0
    day_periods = {}
    for _, (teacher, day, periods, room) in selected_classes:
        if day not in day_periods:
            day_periods[day] = []
        day_periods[day].extend(periods)

    for day in day_periods:
        periods = sorted(set(day_periods[day]))
        if len(periods) > 1:
            for i in range(len(periods) - 1):
                gaps += periods[i + 1] - periods[i] - 1

    # Loại bỏ giáo viên không muốn học
    unwanted_teacher_penalty = sum(1 for _, (teacher, _, _, _) in selected_classes if teacher in UNWANTED_TEACHERS)

    # Loại bỏ phòng không muốn học
    unwanted_room_penalty = sum(1 for _, (_, _, _, room) in selected_classes if room in UNWANTED_ROOMS)

    # Loại bỏ ngày không muốn học
    unwanted_day_penalty = sum(1 for _, (_, day, _, _) in selected_classes if day in UNWANTED_DAYS)


    # Nếu có xung đột, trả về giá trị lớn để loại bỏ cá thể
    if conflicts > 0:
        return 1000, 1000, 1000


    return conflicts, gaps, unwanted_teacher_penalty, unwanted_room_penalty, unwanted_day_penalty


toolbox = base.Toolbox()
toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=[o - 1 for o in COURSE_OPTIONS], indpb=0.2)
toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(42)
    pop = toolbox.population(n=100)
    algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=100, cxpb=0.7, mutpb=0.2, ngen=50, verbose=False)

    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    print(pareto_front)
    print("\n🔹 Các lịch trình tối ưu:")

    for ind in pareto_front:
        schedule = [(USER_INPUT[i], COURSES[USER_INPUT[i]][idx]) for i, idx in enumerate(ind)]
        print(f"📌 Lịch: {schedule}")
        print(f"❌ Xung đột: {ind.fitness.values[0]}")
        print(f"🕐 Khoảng trống: {ind.fitness.values[1]}")
        print(f"🚫 Giáo viên bị cấm: {ind.fitness.values[2]}")
        print(f"🏠 Phòng bị cấm: {ind.fitness.values[3]}")
        print(f"📅 Ngày bị cấm: {ind.fitness.values[4]}\n")


if __name__ == "__main__":
    main()
