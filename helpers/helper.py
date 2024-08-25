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
    jobs_temp = jobs
    dependencies_temp = dict()

    for j in jobs_temp:
        dependencies_temp[j] = j.dependencies

    while len(jobs_temp) > 0:
        # find the job that can be process in parallel
        parallel_jobs = {j for j in jobs_temp if len(j.dependencies) == 0}

        # raise error when cycle is detected
        # cycle is detected when there is leftover node in the graph but parallel jobs is not found
        if len(parallel_jobs) == 0:
            print(f"Cycle detected among {jobs_temp}")
            raise CycleDetected
        
        # append the parallel nodes to the topo order 
        topo_order.append(parallel_jobs)
        
        # remove the independent node from the graph
        jobs_temp = list(set(jobs_temp) - parallel_jobs)

        # remove the dependencies from the rest of the node
        j: Job
        for j in jobs_temp:
            j.dependencies = list(set(j.dependencies) - parallel_jobs)

    for j in jobs:
        j.dependencies = dependencies_temp[j]

    return topo_order

def calculate_make_span(schedule: list, topo_order: list) -> tuple:
    """
    given the schedule, return the team with highest make span and the make span
    
    Returns:
        (Team, make_span)
    """
    total_make_span = 0

    for o in topo_order:
        make_span = [s.make_span for s in schedule if s.job in o]
        total_make_span += max(make_span)
    
    return total_make_span

def calculate_cost(schedule: list, teams: list):
    """
    given the schedule, calculate the total cost
    
    Returns:
        (Team, cost)
    """
    total_cost = 0
    for t in teams:
        cost = sum([s.cost for s in schedule if s.team == t])
        total_cost += cost
    
    return total_cost

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

def find_longest_make_span(schedule: list, teams: list):
    """
    find the team with the longest make span and its make span
    """
    team_make_span = dict()
    for t in teams:
        total_make_span = sum([s.make_span for s in schedule if s.team == t])
        team_make_span[t] = total_make_span
    
    max_team = max(team_make_span, key=team_make_span.get)
    
    return max_team, team_make_span[max_team] 

def find_expensive_cost(schedule: list, teams: list):
    """
    find the team with the most expensive cost and its cost
    """
    team_cost = dict()
    for t in teams:
        total_make_span = sum([s.cost for s in schedule if s.team == t])
        team_cost[t] = total_make_span
    
    max_team = max(team_cost, key=team_cost.get)
    
    return max_team, team_cost[max_team] 

def print_schedule(schedule: list):
    teams = list({s.team for s in schedule})
    jobs = list({s.job for s in schedule})
    topo_order = kahn_sort(jobs)
    
    make_span = calculate_make_span(schedule, topo_order)
    cost = calculate_cost(schedule, teams)

    longest_team, longest_make_span = find_longest_make_span(schedule, teams)
    expensive_team, expensive_cost = find_expensive_cost(schedule, teams)

    print("==================================================================")
    print(f"Total Make span: {make_span:.2f} days")
    print(f"Total Cost: $ {cost:.2f} k")
    print(f"Team {longest_team.name} has the highest make span ({longest_make_span:.2f} days)")
    print(f"Team {expensive_team.name} has the highest cost ($ {expensive_cost:.1f}k)")

    current_phase = JOB_TYPE.PLANNING
    print_phase = True
    for o in topo_order:
        j: Job
        for j in o:
            if j.job_type != current_phase:
                current_phase = j.job_type
                print_phase = True
            
            if print_phase:
                print("")
                print(f"{current_phase.name}")
                print("---------------------------------------")
                print_phase = False
            
            for s in schedule:
                if s.job == j:
                    print(f"{s.team.name} | {s.make_span:.2f} days | $ {s.cost:.1f}k | {j.name}")
                    break
        
        print("---------------------------------------")
        


    
