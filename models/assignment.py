from models.task import Task
from models.member import Member

class Assignment:
    def __init__(self, task: Task, member: Member):
        self.task: Task = task
        self.member: Member = member
        
        self.compatibility = self.check_compatibility()
        self.estimated_time = 1 / self.member.efficiency

    def check_compatibility(self) -> float:
        total_task = len(self.task.skills | self.member.skill_set)
        overlap = len(self.task.skills & self.member.skill_set)
        compatibility = overlap / total_task

        return compatibility