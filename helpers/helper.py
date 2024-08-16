"""
some helper scripts to make my life easier
"""

from models.job import Job, JOB_TYPE
from models.team import Team
import random

def create_random_jobs(amount:int) -> list:
    """
    returns a list of random jobs
    """
    random_jobs = []
    o_durations = [random.randrange(10, 50) for i in range(amount)]
    o_costs = [random.randrange(100, 500) for i in range(amount)]

    for i in range(amount):
        durations = [o_durations[i], o_durations[i]+5, o_durations[i]+10]
        costs = [o_costs[i], o_costs[i]+5, o_costs[i]+10]
        
        new_job = Job(f"job_{i+1}", i+1, JOB_TYPE.PLANNING, durations, costs)
        random_jobs.append(new_job)

    return random_jobs

def create_random_team(amount: int) -> list:
    """
    returns a list of random team
    """
    random_teams = []
    random_time_efficiency = [random.random() for i in range(amount)]
    random_cost_efficiency = [random.random() for i in range(amount)]

    for i in range(amount):
        new_team = Team(f"team_{i+1}", i+1, random_time_efficiency[i], random_cost_efficiency[i], JOB_TYPE.PLANNING)
        random_teams.append(new_team)

    return random_teams


def calculate_make_span(schedule: list) -> tuple:
    """
    given the schedule, return the team with highest make span and the make span
    
    Returns:
        (Team, make_span)
    """
    teams = {s.team for s in schedule}
    make_span = {}

    for t in teams:
        make_span[t] = sum([s.make_span for s in schedule if s.team == t])
    
    max_team = max(make_span, key=make_span.get)
    
    return max_team, make_span[max_team]

def calculate_cost(schedule: list):
    """
    given the schedule, return the team with highest cost and the cost
    
    Returns:
        (Team, cost)
    """
    teams = {s.team for s in schedule}
    cost = {}

    for t in teams:
        cost[t] = sum([s.cost for s in schedule if s.team == t])
    
    max_team = max(cost, key=cost.get)
    total_cost = sum([s.cost for s in schedule])
    
    return max_team, total_cost

def calculate_distribution_penalty(schedule: list, jobs: list, teams: list) -> float:
    """
    calculates the penalty of task distribution
    """
    number_of_jobs = len(jobs)
    number_of_teams = len(teams)
    avg_job_per_team = number_of_jobs / number_of_teams
    
    mean_diff_squared = 0
    for t in teams:
        # j is the number of jobs assinged to the team
        j = len(set([s.job for s in schedule if s.team == t]))
        diff = j - avg_job_per_team
        diff_squared = diff ** 2
        mean_diff_squared += diff_squared / number_of_teams
    
    return mean_diff_squared

def print_schedule(schedule: list):
    schedule.sort(key=lambda x: x.make_span)
    teams = list({s.team for s in schedule})
    teams.sort(key=lambda x: x.name)

    duration_t, make_span = calculate_make_span(schedule)
    cost_t, cost = calculate_cost(schedule)

    print(f"Make span: T {make_span:.2f}")
    print(f"Cost: $ {cost:.2f}")
    print(f"Team {duration_t.name} has the highest make span")
    print(f"Team {cost_t.name} has the highest cost")

    for job_type in JOB_TYPE: 
        print(job_type.name)
        t: Team
        for t in teams:
            job_slot = [s.job.name for s in schedule if s.team == t and s.job.job_type == job_type]
            make_span = sum([s.make_span for s in schedule if s.team == t and s.job.job_type == job_type])
            cost = sum([s.cost for s in schedule if s.team == t and s.job.job_type == job_type])
            print(f"{t.name} | T {make_span:.2f} | $ {cost:.2f} | {job_slot}")
    
