from models.assignment import Assignment
import numpy as np
from models.project import Project

# to maximize - use new-old / old
# to minimize - use old-new / old

def maximize_imp(new:float, old:float) -> float:
    if old == 0:
        # return an arbitary number when the old is 0 to avoid division by zero error
        if new == 0:
            return 0
        return new
    return (new - old) / abs(old)

def minimize_imp(new:float, old:float) -> float:
    if old == 0:
        # return an arbitary number when the old is 0 to avoid division by zero error
        if new == 0:
            return 0
        return new
    return (old - new) / abs(old)

def check_task_compatibility_imp(assignments: list[Assignment], initial_formation: Project) -> float:
    '''return the improvement of new task compatibilitiy to original task compatibility'''
    new_task_compatibility = sum([a.compatibility for a in assignments])
    
    # maximize
    imp = maximize_imp(new_task_compatibility, initial_formation.task_compatility)
    
    return imp

def check_team_size(assignments: list[Assignment], initial_formation: Project) -> float:
    '''check the unique members in the assingment'''
    unique_members = {a.member for a in assignments}
    team_size = len(unique_members)

    team_size_imp = minimize_imp(team_size, initial_formation.team_size)
    return team_size_imp

def check_task_load(assignments: list[Assignment], initial_formation: Project) -> float:
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

    imp = minimize_imp(diff_squared, initial_formation.task_load)    
    return imp

def check_salary_budget_imp(assignments: list[Assignment], initial_formation: Project) -> float:
    '''check the improvement of project budget to total salary'''

    new_total_salary = sum({a.member.salary for a in assignments})
    
    # minimize
    imp = minimize_imp(new_total_salary, initial_formation.total_salary)

    return imp

def check_total_time_imp(assignments: list[Assignment], initial_formation: Project) -> float:
    new_total_time = sum([a.estimated_time for a in assignments])

    # minimize
    imp = minimize_imp(new_total_time, initial_formation.total_estimated_time)

    return imp


def check_collaboration_score_imp(assignments: list[Assignment], initial_formation: Project) -> float:
    new_collab_score = 0
    for a in assignments:
        score = sum([a.member.collaboration_scores[s] for s in a.member.collaboration_scores])
        score /= len(a.member.collaboration_scores) 
        
        new_collab_score += score
    
    imp = maximize_imp(new_collab_score, initial_formation.collab_score)
    
    return imp

def check_fitness(assignments: list[Assignment], initial_formation: Project) -> float:
    '''check the fitness of the solution'''
    fitness = 0
    
    task_compatibility = check_task_compatibility_imp(assignments, initial_formation)
    fitness += task_compatibility

    salary_budget_imp = check_salary_budget_imp(assignments, initial_formation)
    fitness += salary_budget_imp

    task_load_imp = check_task_load(assignments, initial_formation)
    fitness += task_load_imp

    total_time_imp = check_total_time_imp(assignments, initial_formation)
    fitness += total_time_imp

    collab_score_imp = check_collaboration_score_imp(assignments, initial_formation)
    fitness += collab_score_imp

    team_size_imp = check_team_size(assignments, initial_formation)
    fitness += team_size_imp

    return fitness

def average_fitness(solution_fitness: list[float]) -> float:
    avg = np.mean(solution_fitness)

    return avg