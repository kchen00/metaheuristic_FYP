from helpers.helper import create_random_jobs, create_random_team
from models.assignment import Assignment
from scheduler import min_min_scheduler

jobs = create_random_jobs(10)
teams = create_random_team(5)


def run() -> list:
    """
    using brute force to find the schedule with shortest make span
    """
    assignments = []
    for j in jobs:
        for t in teams:
            new_assignment = Assignment(j, t)
            assignments.append(new_assignment)

    solution = min_min_scheduler.min_min(assignments)
    
    return solution
