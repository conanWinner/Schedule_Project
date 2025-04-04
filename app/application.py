import random
from deap import base, creator, tools, algorithms

from service.constraints_service import non_conflict_periods
from constant.constant_variable import user_preferences, PREFERENCE_FUNCTIONS, USER_INPUT, COURSES

NUM_COURSES = len(USER_INPUT)
COURSE_OPTIONS = [len(COURSES[course]) for course in USER_INPUT]  # Số lớp mỗi môn

# Thiết lập NSGA-II
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


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
