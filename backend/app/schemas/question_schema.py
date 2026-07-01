from enum import Enum


class DifficultyEnum(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class ModelEnum(str, Enum):
    llama3 = "llama3"
    gpt4o_mini = "gpt-4o-mini"
