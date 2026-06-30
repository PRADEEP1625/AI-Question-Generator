from enum import Enum


class TopicEnum(str, Enum):
    react = "React"
    python = "Python"
    sql = "SQL"
    javascript = "JavaScript"
    java = "Java"
    dsa = "Data Structures & Algorithms"


class DifficultyEnum(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
