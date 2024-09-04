import config
from models.assignment import Assignment
from helpers import helper
from itertools import product

def evaluate_schedule(schedule, jobs: list, teams: list, job_topo_order: list, make_span_weight: float, cost_weight: float) -> float:
    """
    evaluates the fitness of the solution
    """
    make_span = helper.calculate_make_span(schedule, job_topo_order)
    
    cost = helper.calculate_cost(schedule, teams)

    load_penalty = helper.calculate_distribution_penalty(schedule, jobs, teams)

    risk_penalty = helper.calculate_risk_penalty(schedule, teams)

    parallel_penalty = helper.calculate_parallel_penalty(schedule, teams, job_topo_order)

    fitness = make_span_weight * make_span + cost_weight * cost
    fitness /= sum([make_span_weight, cost_weight])
    
    fitness += load_penalty + risk_penalty + parallel_penalty

    return fitness

def run():
    """
    brute force method to find the best schedule
    """
    jobs = config.jobs
    teams = config.teams
    job_topo_order = helper.kahn_sort(jobs)
    possible_assignments = []
    schedule = []

    make_span_weight = 0.5
    cost_weight = 0.5
    
    previous_best = 99999999999
    
    for j in jobs:
        job_combinations = []
        for t in teams:
            if j.job_type == t.job_focus:
                new_assignment = Assignment(j, t)
                job_combinations.append(new_assignment)
        possible_assignments.append(job_combinations)
    
    combinations_iterator = product(*possible_assignments)
    iteration = 0
    best = None
    for c in combinations_iterator:
        print(f"iteration: {iteration} | previous best: {previous_best}")
        schedule = list(c)
        fitness = evaluate_schedule(schedule, jobs, teams, job_topo_order, make_span_weight, cost_weight)
        if fitness < previous_best:
            print(f"New best found! | {fitness} | {schedule}")
            previous_best = fitness
            best = schedule
        
        iteration += 1
    
    return best
    
run()
