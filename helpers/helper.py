"""
some helper scripts to make my life easier
"""

from models.job import Job, JOB_TYPE
from models.team import Team
import random

class CycleDetected(Exception):
    """
    raised when a cycle is detected in job dependency
    """
    pass

def create_random_jobs(amount:int) -> list:
    """
    returns a list of random jobs
    """
    random_jobs = []
    o_durations = [random.uniform(10, 50) for i in range(amount)]
    o_costs = [random.uniform(100, 500) for i in range(amount)]
    risks = [random.uniform(0.1, 0.9) for i in range(amount)]

    for i in range(amount):
        durations = [o_durations[i], o_durations[i]+5, o_durations[i]+10]
        costs = [o_costs[i], o_costs[i]+5, o_costs[i]+10]
        
        new_job = Job(f"job_{i+1}", i+1, JOB_TYPE.PLANNING, durations, costs, risks[i])
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

def kahn_sort(jobs: list) -> list:
    """
    using kahn algorithm to topological sort the jobs

    return a list of set containing jobs that can be processed in parallel in each level
    """
    topo_order = []

    while len(jobs) > 0:
        # find the job that can be process in parallel
        parallel_jobs = {j for j in jobs if len(j.dependencies) == 0}

        # raise error when cycle is detected
        # cycle is detected when there is leftover node in the graph but parallel jobs is not found
        if len(parallel_jobs) == 0:
            print(f"Cycle detected among {jobs}")
            raise CycleDetected
        
        # append the parallel nodes to the topo order 
        topo_order.append(parallel_jobs)
        
        # remove the independent node from the graph
        jobs = list(set(jobs) - parallel_jobs)

        # remove the dependencies from the rest of the node
        j: Job
        for j in jobs:
            j.dependencies = list(set(j.dependencies) - parallel_jobs)

    return topo_order

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

def calculate_risk_penalty(schedule: list, teams: list) -> float:
    """
    calculate the risk of the schedule based on the job and team distribution
    """
    sum_of_job_risk = sum([s.job.risk for s in schedule])
    mean_of_risk = sum_of_job_risk / len(teams)

    mean_diff_squared = 0
    for t in teams:
        team_job_risk = sum([s.job.risk for s in schedule if s.team == t])
        diff = team_job_risk - mean_of_risk
        diff_squared = diff ** 2
        mean_diff_squared += diff_squared
    
    return mean_diff_squared

def calculate_parallel_penalty(schedule: list, teams: list, topo_order: list) -> float:
    """
    calculate the penalty of job and team assigment based on the parallel distribution of the jobs
    """
    penalty = 0.0
    for t in teams:
        job = {s.job for s in schedule if s.team == t}
        # only check when the team is assigned with multiple jobs
        if len(job) > 1:
            for o in topo_order:
                if job <= o and len(o) > 1:
                    penalty += len(job) ** 2

    return penalty

def print_schedule(schedule: list):
    schedule.sort(key=lambda x: x.make_span)
    teams = list({s.team for s in schedule})
    teams.sort(key=lambda x: x.name)

    duration_t, make_span = calculate_make_span(schedule)
    cost_t, cost = calculate_cost(schedule)

    print("==================================================================")
    print(f"Make span: {make_span:.2f} days")
    print(f"Cost: $ {cost:.2f}k")
    print(f"Team {duration_t.name} has the highest make span")
    print(f"Team {cost_t.name} has the highest cost")

    for job_type in JOB_TYPE: 
        print(job_type.name)
        t: Team
        for t in teams:
            if t.job_focus == job_type:
                job_slot = [s.job for s in schedule if s.team == t and s.job.job_type == job_type]
                make_span = sum([s.make_span for s in schedule if s.team == t and s.job.job_type == job_type])
                cost = sum([s.cost for s in schedule if s.team == t and s.job.job_type == job_type])
                print(f"{t.name} | {make_span:.2f} days | $ {cost:.1f}k | {job_slot}")
        print("")
    
