from models.assignment import Assignment
from models.task import Task
import os, pickle
from itertools import combinations

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
    
    def formation_metrics(self) -> dict:
        return {
            "task compatibility": self.task_compatility,
            "team size": self.team_size,
            "task load": self.task_load,
            "harmony among team member": self.collab_score,
            "total salary": self.total_salary,
            "estimated total time": self.total_estimated_time,
        }

    def assingment_member(self) -> dict:
        return {
            a.task.name: a.member.name for a in self.assignments
        }

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
        members = {a.member for a in self.assignments}
        member_combinations = combinations(members, 2)
        n = 0
        for m_comb in member_combinations:
            score = m_comb[0].collaboration_scores[m_comb[1]] + m_comb[1].collaboration_scores[m_comb[0]]
            average = score / 2
            collab_score += average
            n += 1
        
        if n > 0:
            collab_score /= n
    
        return collab_score

    def get_team_size(self) -> int:
        '''get the team size for this project'''
        members = set(a.member for a in self.assignments)
        team_size = len(members)

        return team_size
    
    def save_project(self, before: bool = False, mh_name: str = ""):
        '''save the project object into a pickle file'''
        if before:
            save_path = f"data/solution/before/{self.name}"
            if not(os.path.exists(save_path)):
                os.makedirs(save_path)
            with open(f"{save_path}/{self.name}.pickle", "wb") as f:
                pickle.dump(self, f)

        else:
            save_path = f"data/solution/after/{self.name}"
            if not(os.path.exists(save_path)):
                os.makedirs(save_path)
            with open(f"{save_path}/{mh_name}.pickle", "wb") as f:
                pickle.dump(self, f)
