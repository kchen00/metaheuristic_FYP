from models.assignment import Assignment

class Project:
    def __init__(self, name: str, assignments: list[Assignment]):
        self.name = name
        self.assignments: list[Assignment] = assignments