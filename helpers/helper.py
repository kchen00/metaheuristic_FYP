"""
some helper scripts to make my life easier
"""

from models.job import Job, JOB_TYPE
from models.employee import Rank
import random
import numpy as np

class CycleDetected(Exception):
    """
    raised when a cycle is detected in job dependency
    """
    pass

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
    given the schedule, return the make span
    """
    total_make_span = 0

    for o in topo_order:
        make_span = [s.make_span for s in schedule if s.job in o]
        total_make_span += max(make_span)
    
    return total_make_span

def calculate_cost(formation: list, employees: list):
    """
    given the formation, calculate the total cost
    """
    total_cost = 0
    for e in employees:
        cost = sum([f.cost for f in formation if f.employee == e])
        total_cost += cost
    
    return total_cost

def calculate_distribution_penalty(formation: list, jobs: list, employees: list) -> float:
    """
    calculates the penalty of task distribution
    """
    number_of_jobs = len(jobs)
    number_of_employees = len(employees)
    avg_job_per_person = number_of_jobs / number_of_employees
    
    mean_diff_squared = 0
    for e in employees:
        # j is the number of jobs assinged to the team
        j = len(set([f.job for f in formation if f.employee == e]))
        diff = j - avg_job_per_person
        diff_squared = diff ** 2
        mean_diff_squared += diff_squared / number_of_employees
    
    return mean_diff_squared

def calculate_risk_penalty(formation: list, employees: list) -> float:
    """
    calculate the risk of the schedule based on the job and team distribution
    """
    sum_of_job_risk = sum([f.risk for f in formation])
    mean_of_risk = sum_of_job_risk / len(employees)

    mean_diff_squared = 0
    for e in employees:
        team_job_risk = sum([f.risk for f in formation if f.employee == e])
        diff = team_job_risk - mean_of_risk
        diff_squared = diff ** 2
        mean_diff_squared += diff_squared
    
    return mean_diff_squared

def calculate_parallel_penalty(formation: list, employees: list, topo_order: list) -> float:
    """
    calculate the penalty of job and employee assigment based on the parallel distribution of the jobs
    """
    penalty = 0.0
    for e in employees:
        job = {f.job for f in formation if f.employee == e}
        # only check when the team is assigned with multiple jobs
        if len(job) > 1:
            for o in topo_order:
                # if the job assigned to the employee is the subset of one of kahn sort set
                # and the number of jobs is more than 1 (no penalty if employee is only given 1 job)
                # then there is penalty
                if job <= o and len(o) > 1:
                    penalty += len(job) ** 2

    return penalty

def calculate_risk_rank_ratio_penalty(formation: list, employees: list) -> float:
    """
    calculate the penalty to risk rank ratio
    """
    mean_diff_squared = 0.0
    mean_ratio = np.mean([f.risk_rank_ratio for f in formation])
    for e in employees:
        employee_sum = sum([f.risk_rank_ratio for f in formation if f.employee == e])
        diff = employee_sum - mean_ratio
        diff_squared = diff ** 2
        mean_diff_squared += diff_squared

    return mean_diff_squared

def find_longest_make_span(formation: list, employees: list):
    """
    find the employee with the longest make span and its make span
    """
    employee_make_span = dict()
    for e in employees:
        total_make_span = sum([f.make_span for f in formation if f.employee == e])
        employee_make_span[e] = total_make_span
    
    max_team = max(employee_make_span, key=employee_make_span.get)
    
    return max_team, employee_make_span[max_team] 

def find_expensive_cost(formation: list, employees: list):
    """
    find the team with the most expensive cost and its cost
    """
    employee_cost = dict()
    for e in employees:
        total_cost = sum([f.cost for f in formation if f.employee == e])
        employee_cost[e] = total_cost
    
    max_employee = max(employee_cost, key=employee_cost.get)
    
    return max_employee, employee_cost[max_employee] 

def print_formation(formation: list):
    employee = list({f.employee for f in formation})
    jobs = list({f.job for f in formation})
    topo_order = kahn_sort(jobs)
    
    make_span = calculate_make_span(formation, topo_order)
    cost = calculate_cost(formation, employee)

    longest_employee, longest_make_span = find_longest_make_span(formation, employee)
    expensive_employee, expensive_cost = find_expensive_cost(formation, employee)

    senior = 0
    junior = 0

    for e in set(f.employee for f in formation):
        match e.rank:
            case Rank.JUNIOR:
                junior += 1
            case Rank.SENIOR:
                senior += 1         

    print("==================================================================")
    print(f"Total Make span: {make_span:.2f} days")
    print(f"Total Cost: $ {cost:.2f} k")
    print(f"Employee {longest_employee.name} has the highest make span ({longest_make_span:.2f} days)")
    print(f"Employee {expensive_employee.name} has the highest cost ($ {expensive_cost:.1f}k)")

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
            
            for f in formation:
                if f.job == j:
                    print(f"{f.employee.name} ({f.employee.rank}) | {f.make_span:.2f} days | $ {f.cost:.1f}k | {j.name} ({j.risk})")
                    break
        
        print("---------------------------------------")
    
    print(f"{senior} senior | {junior} junior")