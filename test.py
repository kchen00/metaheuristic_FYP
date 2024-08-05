from helpers import helper
from models.assignment import Assignment
import random
from scheduler import min_min_scheduler

teams = helper.create_random_team(4)
jobs = helper.create_random_jobs(10)

assignments = []

for j in jobs:
    for t in teams:
        new_assignment = Assignment(j, t)
        new_assignment.active = random.choice([True, False])
        assignments.append(new_assignment)

schedule = min_min_scheduler.min_min(assignments)
helper.print_schedule(schedule)
