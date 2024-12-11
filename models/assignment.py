from models.task import Task
from models.member import Member

class Assignment:
    def __init__(self, task: Task, member: Member):
        self.task: Task = task
        self.member: Member = member
        self.compatibility = 0.0
        
        self.check_compatibility()

    def check_compatibility(self) -> float:
        total_task = len(self.task.skills | self.member.skill_set)
        overlap = len(self.task.skills & self.member.skill_set)
        self.compatibility = overlap / total_task

        return self.compatibility