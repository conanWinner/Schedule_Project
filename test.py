import random
from deap import base, creator, tools, algorithms
import numpy as np

# Thiết lập tham số
NUM_CLASSES = 3
NUM_ROOMS = 3
NUM_TIMES = 3
POP_SIZE = 50
NGEN = 50

# Định nghĩa cấu trúc tối ưu hóa
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)


# Hàm khởi tạo cá thể
def init_individual():
    return creator.Individual(
        [(random.randint(0, NUM_ROOMS - 1), random.randint(0, NUM_TIMES - 1)) for _ in range(NUM_CLASSES)])


# Hàm đánh giá
def evaluate(individual):
    # Mục tiêu 1: Đếm số xung đột phòng
    conflicts = 0
    room_time = {}
    for class_idx, (room, time) in enumerate(individual):
        key = (room, time)
        if key in room_time:
            conflicts += 1
        else:
            room_time[key] = True

    # Mục tiêu 2: Đếm số khung giờ liên tiếp của giáo viên
    teacher_load = 0
    times = sorted([t for _, t in individual[:2]])  # Giả sử C1, C2 do G1 dạy
    if len(times) > 1 and times[1] == times[0] + 1:
        teacher_load += 1

    return conflicts, teacher_load


# Hàm đột biến tùy chỉnh
def mutate_individual(individual):
    for i in range(len(individual)):
        if random.random() < 0.2:  # Xác suất đột biến 20%
            individual[i] = (random.randint(0, NUM_ROOMS - 1), random.randint(0, NUM_TIMES - 1))
    return individual,


# Thiết lập toolbox
toolbox = base.Toolbox()
toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_individual)  # Sử dụng hàm đột biến tùy chỉnh
toolbox.register("select", tools.selNSGA2)


# Chạy thuật toán
def main():
    random.seed(42)
    pop = toolbox.population(n=POP_SIZE)

    # Chạy NSGA-II
    algorithms.eaMuPlusLambda(pop, toolbox, mu=POP_SIZE, lambda_=POP_SIZE,
                              cxpb=0.7, mutpb=0.2, ngen=NGEN,
                              stats=None, halloffame=None, verbose=True)

    # Lấy Pareto Front
    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]

    # In kết quả
    print("\nCác giải pháp tốt nhất (Pareto Front):")
    for ind in pareto_front:
        print(f"Lịch trình: {ind}, Xung đột: {ind.fitness.values[0]}, Tải giáo viên: {ind.fitness.values[1]}")


if __name__ == "__main__":
    main()