from helpers import helper
from models.job import Job, JOB_TYPE
from models.team import Team
from models.assignment import Assignment
import random
import numpy as np
from matplotlib import pyplot as plt

class State(Assignment):
    def __init__(self, j: Job, t: Team):
        super().__init__(j, t)

class Solution:
    """
    represent a possible solution in search space
    """
    def __init__(self, state: list):
        self.state = state
        self.fitness = 0
        
        self.make_span = 0
        self.cost = 0
        
        self.selected = 1

class Anneal:
    """
    represent the simulated annealing process
    """
    def __init__(self, jobs: list, teams: list, cooling_rate: float = 0.95, temperature: float = 1, make_span_weight: float = 0.5, cost_weight: float = 0.5) -> None:
        self.jobs = jobs
        self.teams = teams

        self.iteration = 1
        self.cooling_rate = cooling_rate
        self.temperature = temperature

        self.make_span_weight = make_span_weight
        self.cost_weight = cost_weight
        
        # the current candidate that is being evaluated
        self.current = None
        # the neighbbour solution
        self.neighbour = None
        # the best candidate overall
        self.best = None
        self.hist = []
    
    def create_initial_solution(self) -> Solution:
        """
        creates the initial solution
        """
        state = []

        for j in self.jobs:
            # assign random team to the job
            selected_team = random.choice([t for t in self.teams if t.job_focus == j.job_type])
            new_state = State(j, selected_team)
            state.append(new_state)
        
        current = Solution(state)
        return current

    def evaluate_candidate(self, candidate: Solution):
        """
        evaluates the candidate solution
        """
        # fitness in terms of make span
        make_span_t, make_span = helper.calculate_make_span(candidate.state)
        cost_t, cost = helper.calculate_cost(candidate.state)
        candidate.make_span = make_span
        candidate.cost = cost

        candidate.fitness = make_span * self.make_span_weight + cost * self.cost_weight
        candidate.fitness /= sum([self.make_span_weight, self.cost_weight])
        
    def create_neighbour_solution(self, change_prob: float) -> Solution:
        """
        based on the current solution create a neighbour solution by randomly assign new team to the job

        the amount of changes depends on the change_prob
        """
        state = []

        s: State
        for s in self.current.state:
            new_state = State(s.job, s.team)
            if random.random() < change_prob:
                selected_team = random.choice([t for t in self.teams if t.job_focus == s.job.job_type])
                new_state.team = selected_team
            
            state.append(new_state)
                    
        neighbour = Solution(state)
        return neighbour
    
    def decide_solution(self):
        """
        accepts the neighbour solution based on probability
        """
        diff = self.neighbour.fitness - self.current.fitness
        # if the diff is negative, means that neighbour is better than current solution
        # always accept the solution when diff < 0
        # no need to evaluate when diff == 0
        if diff < 0:
            self.current = self.neighbour
        else:
            accept_prob = np.exp(-diff/self.temperature)
            # else ask RNG god whether or not to accept the worse solution
            if random.random() < accept_prob and diff > 0:
                print("RNG god accepts the worse solution")
                self.current = self.neighbour
        
        # keeping track of the best solution 
        if self.iteration == 1:
            self.best = self.current
            print(f"New best found! | {self.best.state}")
        else:
            if self.current.fitness < self.best.fitness:
                self.best = self.current
                self.best.selected = self.iteration
                print(f"New best found! | {self.best.state}")
        
        self.hist.append(self.current.fitness)

    def cool_down(self):
        self.temperature *= self.cooling_rate
        self.temperature = max(0.1, self.temperature)

def run():
    jobs = helper.create_random_jobs(10)
    teams = helper.create_random_team(5)

    anneal = Anneal(jobs, teams, cooling_rate=0.95, temperature=2)
    anneal.current = anneal.create_initial_solution()
    anneal.evaluate_candidate(anneal.current)
    
    for i in range(50):
        print(f"iteration {anneal.iteration} | temp: {anneal.temperature}")
        anneal.neighbour = anneal.create_neighbour_solution(anneal.temperature)
        anneal.evaluate_candidate(anneal.neighbour)
        anneal.decide_solution()
        anneal.cool_down()

        anneal.iteration += 1
    
    plt.plot(anneal.hist)
    plt.show()
    
    return anneal.best

def test():
    temp = 5
    accept_prob = []
    for i in range(100):
        diff = 3
        prob = np.exp(-diff / temp)
        accept_prob.append(prob)
        temp *= 0.96
    
    plt.plot(accept_prob)
    plt.show()
    

