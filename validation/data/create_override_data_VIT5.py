import random
from collections import defaultdict

import pandas as pd

data_df_subjects_teacher = pd.read_excel("./output/hoc_phan_giang_vien_khong_trung.xlsx")
data_df_rooms = pd.read_excel("./output/phong_khong_trung_lap.xlsx")

# Danh sách dữ liệu để random
subjects = data_df_subjects_teacher['Tên học phần'].dropna().unique().tolist()
teachers = data_df_subjects_teacher['Giảng viên'].dropna().unique().tolist()
rooms = data_df_rooms['Số phòng'].dropna().unique().tolist()
days = ["thứ 2", "thứ 3", "thứ 4", "thứ 5", "thứ 6", " thứ 7"]
session = ["buổi sáng", "buổi chiều"]
areas = ["K", "V"]
connectors = [", ", ". ", " và ", " hoặc ", " "]
subject_teacher_pairs = data_df_subjects_teacher[['Tên học phần', 'Giảng viên']].dropna().drop_duplicates().values.tolist()

# Tạo ánh xạ: môn học → danh sách giảng viên
subject_to_teachers = defaultdict(list)
for subject, teacher in subject_teacher_pairs:
    subject_to_teachers[subject].append(teacher)
# Mẫu câu đa dạng
sentence_templates = [
    lambda: f"Tôi thích học sáng {random.choice(days)} với {random.randint(1,2)} môn là hợp lý",
    lambda: f"Tôi ưu tiên học chiều {random.choice(days)} khoảng {random.randint(1,3)} môn",
    lambda: f"Tôi không muốn học vào cuối tuần như {random.choice(['thứ 7', 'thứ 6'])}",
    lambda: f"Tôi muốn học ở khu vực {random.choice(areas)} vì tiện đi lại",
    lambda: (lambda d1: f"Tôi chỉ muốn học tối đa {random.randint(2,3)} môn mỗi ngày {d1} và ngày {random.choice([d for d in days if d != d1])}")(random.choice(days)),
    lambda: f"Tôi thích học sáng {random.choice(days)} với {random.choice(teachers)} môn {random.choice(subjects)} tại phòng {random.choice(areas)}.{random.choice(rooms)}",
    lambda: f"Tôi tránh học với {random.choice(teachers)} vì không phù hợp thời gian",
    lambda: f"Tôi không thích học ở phòng {random.choice(areas)}.{random.choice(rooms)} vào ngày {random.choice(days)} vì hơi ồn",
    lambda: f"Tôi cần nghỉ ít nhất {random.randint(1,2)} tiết giữa các môn vào ngày {random.choice(days)} để di chuyển",
    lambda: f"Tôi muốn bắt đầu học từ tiết {random.randint(2,4)} trở đi vào ngày {random.choice(days)}",
    lambda: f"Tôi thích học sau {random.randint(8,10)} giờ sáng ngày {random.choice(days)} để có thời gian chuẩn bị",
    lambda: f"Tôi chỉ học chiều {random.choice(days)} nếu không còn lựa chọn nào khác",
    lambda: f"Tôi muốn học ở phòng {random.choice(areas)}.{random.choice(rooms)} vì thoáng mát",
    lambda: f"Tôi muốn học với {random.choice(teachers)} vì thầy/cô giảng hay",
    lambda: f"Tôi muốn học môn {random.choice(subjects)} vào sáng {random.choice(days)} nếu có thể",
    lambda: f"Tôi muốn học sáng ngày {random.choice(days)} ở khu {random.choice(areas)} vì gần nhà bạn",
    lambda: f"Tôi tránh học ở khu vực {random.choice(areas)} ngày {random.choice(days)} do đường đông",
    lambda: f"Tôi ưu tiên các môn {random.randint(1,4)} tiết vào buổi chiều ngày {random.choice(days)}",
    lambda: f"Tôi thích lịch học trải đều trong tuần, mỗi ngày khoảng {random.randint(2,3)} môn",
    lambda: f"Tôi muốn nghỉ giữa các môn ít nhất {random.randint(1,2)} tiết nếu có thể",
    lambda: f"Tôi không muốn học sáng {random.choice(days)} vì có công việc cá nhân",
    lambda: f"Tôi thích học ở khu vực {random.choice(areas)} vào buổi chiều",
    lambda: (lambda t1: f"Tôi muốn tránh các tiết học từ tiết {t1} đến tiết {t1 + random.randint(1,2)}" + (f" {random.choice(days)}" if random.choice([True, False]) else ""))(random.randint(1,8)),
    lambda: f"Tôi muốn học từ tiết {random.randint(3,5)} trở đi là hợp lý",
    lambda: f"Tôi không muốn học từ tiết 1 vì tôi không phải người dậy sớm",
    lambda: f"Tôi thích lịch học không quá dày trong ngày, tối đa {random.randint(2,3)} môn",
    lambda: (lambda subject: (
        (lambda t1, t2: f"Tôi muốn học môn {subject} với {t1}" + (f" hoặc {t2}" if t2 else ""))
        (*get_two_teachers_for_subject(subject))
    ))(random.choice(list(subject_to_teachers.keys()))),
    lambda: f"Tôi thích học sáng {random.choice(days)} miễn là có thời gian nghỉ giữa các môn",
    lambda: f"Tôi tránh học với {random.choice(teachers)} vào {random.choice(days)}",
    lambda: f"Tôi chỉ muốn học ở phòng {random.choice(areas)}.{random.choice(rooms)} vào ngày {random.choice(days)} nếu có đủ chỗ ngồi",
    lambda: f"Tôi muốn học môn {random.choice(subjects)} vào buổi sáng {random.choice(days)}",
    lambda: f"Tôi tránh học chiều muộn {random.choice(days)} vì tôi có lịch làm thêm",
    lambda: f"Tôi thích học từ tiết {random.randint(2,4)} đến tiết {random.randint(5,6)} ngày {random.choice(days)}",
    lambda: f"Tôi muốn học môn {random.choice(subjects)} vào thứ {random.randint(2,7)} và có nghỉ giữa giờ",
    lambda: f"Tôi chỉ học buổi sáng trong tuần, không học buổi chiều",
    lambda: (lambda subject, teacher: f"Tôi muốn học {subject} vào sáng {random.choice(days)} nếu có {teacher}")(*random.choice(subject_teacher_pairs)),
    lambda: f"Tôi muốn học môn {random.choice(subjects)} sáng {random.choice(days)}, tránh chiều",
    lambda: f"Tôi không muốn học môn {random.choice(subjects)} vào thứ {random.randint(5,7)}",
    lambda: f"Tôi thích học ở khu {random.choice(areas)} ngày {random.choice(days)} nếu được chọn",
    lambda: f"Tôi chỉ học tối đa {random.randint(1,2)} môn vào chiều {random.choice(days)}",
    lambda: f"Tôi muốn nghỉ ít nhất {random.randint(1,2)} tiết giữa các lớp ngày {random.choice(days)}",
    lambda: f"Tôi ưu tiên học môn {random.choice(subjects)} ở khu {random.choice(areas)}",
    lambda: f"Tôi không thích học môn {random.choice(subjects)} với {random.choice(teachers)}",
    lambda: f"Tôi tránh học ở {random.choice(areas)}.{random.choice(rooms)} nếu có lựa chọn khác",
    lambda: f"Tôi thích học buổi sáng nếu lớp ở phòng {random.choice(areas)}.{random.choice(rooms)}",
    lambda: f"Tôi chỉ học nếu lớp bắt đầu sau {random.randint(8,10)} giờ sáng",
    lambda: f"Tôi muốn học môn {random.choice(subjects)} nhưng không phải sáng {random.choice(days)}",
    lambda: f"Tôi muốn học lớp của {random.choice(teachers)} vào chiều {random.choice(days)}",
    lambda: f"Tôi muốn lịch học nhẹ vào {random.choice(days)}, tối đa {random.randint(1,2)} môn"
]

def get_two_teachers_for_subject(subject):
    teachers = list(set(subject_to_teachers[subject]))  # loại trùng
    if len(teachers) == 0:
        return ("[Không rõ]", None)
    elif len(teachers) == 1:
        return (teachers[0], None)
    else:
        t1 = random.choice(teachers)
        t2 = random.choice([t for t in teachers if t != t1])
        return (t1, t2)


#
# N8N CHAT => LÀM NUỘT PROMPT => GEMINI => JSON

# LÀM NUỘT PROMPT , JSON => VIT5
# 1500 + 500

# Tạo 4000 prompt, không lặp lại câu trong cùng prompt
prompts = []
for _ in range(2000):
    num_sentences = random.randint(1, 5)
    used_sentences = set()
    unique_sentences = []

    # Sinh ra các câu không trùng nhau
    while len(unique_sentences) < num_sentences:
        sentence = random.choice(sentence_templates)()
        if sentence not in used_sentences:
            used_sentences.add(sentence)
            unique_sentences.append(sentence)

    # Chọn connectors ngẫu nhiên
    selected_connectors = [random.choice(connectors) for _ in range(num_sentences - 1)]

    # Nối các câu lại với nhau
    prompt = unique_sentences[0]
    for i in range(1, num_sentences):
        prompt += selected_connectors[i - 1] + unique_sentences[i]

    prompts.append(prompt)

# In thử 10 prompt đầu
# for i, p in enumerate(prompts[:10], 1):
#     print(f"{i:02d}. {p}")

# (Tùy chọn) Ghi ra file CSV
pd.DataFrame({'Kết quả': prompts}).to_excel("./output/Final_Override_Dataset_VIT5.xlsx", index=False)