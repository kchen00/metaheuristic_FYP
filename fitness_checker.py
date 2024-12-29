from models.assignment import Assignment
import numpy as np
from models.project import Project
from setup import project

# to maximize - use new-old / old
# to minimize - use old-new / old

def maximize_imp(new:float, old:float):
    return (new - old) / abs(old)

def minimize_imp(new:float, old:float):
    return (old - new) / abs(old)

def check_task_compatibility_imp(assignments: list[Assignment], current_solution: Project = project) -> float:
    '''return the improvement of new task compatibilitiy to original task compatibility'''
    new_task_compatibility = sum([a.compatibility for a in assignments])
    
    # maximize
    imp = maximize_imp(new_task_compatibility, current_solution.task_compatility)
    
    return imp

def check_team_size(assignments: list[Assignment], current_solution: Project = project) -> float:
    '''check the unique members in the assingment'''
    unique_members = {a.member for a in assignments}
    team_size = len(unique_members)

    team_size_imp = minimize_imp(team_size, current_solution.team_size)
    return team_size_imp

def check_task_load(assignments: list[Assignment], current_solution: Project = project) -> float:
    '''return the improvement of old task load to new task load'''
    # the mean load for each member in this assignments 
    members = set(a.member for a in assignments)
    total_time = sum(a.estimated_time for a in assignments)
    average_time = total_time / len(members)

    diffs = list()
    # calculating load variance
    for m in members:
        processing_time = sum([a.estimated_time for a in assignments if a.member == m])
        diff = processing_time - average_time
        diffs.append(diff ** 2)

    diff_squared = sum(diffs) / len(members)

    imp = minimize_imp(diff_squared, current_solution.task_load)    
    return imp

def check_salary_budget_imp(assignments: list[Assignment], current_solution: Project = project) -> float:
    '''check the improvement of project budget to total salary'''

    new_total_salary = sum({a.member.salary for a in assignments})
    
    # minimize
    imp = minimize_imp(new_total_salary, current_solution.total_salary)

    return imp

def check_total_time_imp(assignments: list[Assignment], current_solution: Project = project) -> float:
    new_total_time = sum([a.estimated_time for a in assignments])

    # minimize
    imp = minimize_imp(new_total_time, current_solution.total_estimated_time)

    return imp


def check_collaboration_score_imp(assignments: list[Assignment], current_solution: Project = project) -> float:
    new_collab_score = 0
    for a in assignments:
        score = sum([a.member.collaboration_scores[s] for s in a.member.collaboration_scores])
        score /= len(a.member.collaboration_scores) 
        
        new_collab_score += score
    
    imp = maximize_imp(new_collab_score, current_solution.collab_score)
    
    return imp

def check_fitness(assignments: list, current_solution: Project = project) -> float:
    '''check the fitness of the solution'''
    fitness = 0
    
    task_compatibility = check_task_compatibility_imp(assignments, current_solution)
    fitness += task_compatibility

    salary_budget_imp = check_salary_budget_imp(assignments, current_solution)
    fitness += salary_budget_imp

    task_load_imp = check_task_load(assignments, current_solution)
    fitness += task_load_imp

    total_time_imp = check_total_time_imp(assignments, current_solution)
    fitness += total_time_imp

    collab_score_imp = check_collaboration_score_imp(assignments, current_solution)
    fitness += collab_score_imp

    return fitness
