from dataclasses import dataclass
from typing import List

@dataclass
class ClassInfo:
    class_index: str
    language: str
    field: str
    sub_topic: str
    teacher: str
    day: str
    periods: List[int]
    area: str
    room: str
    class_size: int