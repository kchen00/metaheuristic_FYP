from models.assignment import Assignment
from models.task import Task

class Project:
    def __init__(self, name: str, assignments: list[Assignment]):
        self.name = name
        self.assignments: list[Assignment] = assignments
        
        # various project stats
        self.total_salary = self.get_total_salary()
        self.task_compatility = self.get_task_compatibility()
        self.task_load = self.get_task_load()
        self.total_estimated_time = self.get_total_estimated_time()
        self.collab_score = self.get_collaboration_score()
        self.team_size = self.get_team_size()

    def print_project(self):
        print("-----------------------------------")
        for a in self.assignments:
            print(f"{a.task.name} -> {a.member.name}", [s.name for s in a.task.skills & a.member.skill_set])
        
        print("-----------------------------------")
        print(f"task compatibility:  {self.task_compatility:.4f}")
        print(f"team size:  {len({a.member for a in self.assignments})}")
        print("communication:  ")
        print(f"task load:  {self.task_load:.4f}")
        print(f"harmony among team member:  {self.collab_score:.4f}")
        print(f"team member motivation:  ")
        print("leader:")
        print("")
        print(f"total salary:  {self.total_salary:.2f}")
        print(f"estimated total time:  {self.total_estimated_time:.4f}")
    
    def get_member(self, task: Task) -> list:
        return [a.member.name for a in self.assignments if a.task == task]
    
    def get_total_salary(self) -> float:
        '''get the total salary of this project'''
        total_salary = sum({a.member.salary for a in self.assignments})
        return total_salary
    
    def get_task_compatibility(self) -> float:
        '''get the total average task compatibilitiy of this project'''
        task_compatility = sum([a.compatibility for a in self.assignments])
        return task_compatility
    
    def get_task_load(self) -> float:
        '''get the average task load of this project'''
        # the average  load for each member in this assignments 
        members = set(a.member for a in self.assignments)
        total_time = sum(a.estimated_time for a in self.assignments)
        average_time = total_time / len(members)

        diffs = list()
        # calculating load variance
        for m in members:
            processing_time = sum([a.estimated_time for a in self.assignments if a.member == m])
            diff = processing_time - average_time
            diffs.append(diff ** 2)

        diff_squared = sum(diffs) / len(members)

        return diff_squared
    
    def get_total_estimated_time(self) -> float:
        '''get estimated time needed of this project'''
        total_estimated_time = sum([a.estimated_time for a in self.assignments])

        return total_estimated_time

    def get_collaboration_score(self) -> float:
        '''get the average collaboration score for this project'''
        collab_score = 0
        for a in self.assignments:
            score = sum([a.member.collaboration_scores[s] for s in a.member.collaboration_scores])
            score /= len(a.member.collaboration_scores) 
            
            collab_score += score
        
        return collab_score

    def get_team_size(self) -> int:
        '''get the team size for this project'''
        members = set(a.member for a in self.assignments)
        team_size = len(members)

        return team_size
    
