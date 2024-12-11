from models.task import Task
from models.member import Member
from models.assignment import Assignment
import numpy as np

def avg_task_compatibility(assignments: list[Assignment]) -> float:
    avg_task_compatibility = np.mean([a.compatibility for a in assignments])

    return avg_task_compatibility

def team_size(assignments: list[Assignment]) -> float:
    unique_members = set([a.member for a in assignments])
    team_size = len(unique_members)

    return team_size

def task_load(assignments: list[Assignment]) -> float:
    tasks = set(a.task for a in assignments)
    members = set(a.member for a in assignments)

    task_per_member = dict()
    for m in members:
        task_per_member[m] = len([a for a in assignments if a.member == m])

    avg_task_per_person = len(tasks) / len(members)
    square_difference = [
        (task_per_member[m] - avg_task_per_person)**2 for m in members
    ] 
    mean_difference = np.mean(square_difference)

    return mean_difference


def check_fitness(assignments: list) -> float:
    fitness = 0
    
    average_compatibility = avg_task_compatibility(assignments)
    fitness += average_compatibility

    task_load_fitness = task_load(assignments)
    fitness -= task_load_fitness
    
    return fitness
