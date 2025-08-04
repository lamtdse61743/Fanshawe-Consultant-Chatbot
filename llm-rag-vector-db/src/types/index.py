from typing import List, Dict, Any

class Vector:
    def __init__(self, values: List[float]):
        self.values = values

class Document:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer