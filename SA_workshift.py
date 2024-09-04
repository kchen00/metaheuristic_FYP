from helpers import helper
from models.job import Job
from models.team import Team
from models.assignment import Assignment
import random
import numpy as np
from matplotlib import pyplot as plt
import config

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
        self.load_balance = 0 
        self.risk_balance = 0
        self.parallel = 0
        
        self.selected = 1

class Anneal:
    """
    represent the simulated annealing process
    """
    def __init__(self, jobs: list, teams: list, cooling_rate: float = 0.95, temperature: float = 1, make_span_weight: float = 0.5, cost_weight: float = 0.5) -> None:
        self.jobs = jobs
        self.teams = teams
        self.job_topo_order = helper.kahn_sort(self.jobs)

        self.iteration = 1
        self.cooling_rate = cooling_rate
        self.temperature = temperature

        self.make_span_weight = make_span_weight
        self.cost_weight = cost_weight
        
        # the current candidate that is being evaluated
        self.current = None
        # the neighbbour solution
        self.neighbours = [] 
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
        make_span = helper.calculate_make_span(candidate.state, self.job_topo_order)
        candidate.make_span = make_span
        
        cost = helper.calculate_cost(candidate.state, self.teams)
        candidate.cost = cost

        load_penalty = helper.calculate_distribution_penalty(candidate.state, self.jobs, self.teams)
        candidate.load_balance = load_penalty

        risk_penalty = helper.calculate_risk_penalty(candidate.state, self.teams)
        candidate.risk_balance = risk_penalty

        parallel_penalty = helper.calculate_parallel_penalty(candidate.state, self.teams, self.job_topo_order)
        candidate.parallel = parallel_penalty

        candidate.fitness = self.make_span_weight * make_span + self.cost_weight * cost
        candidate.fitness /= sum([self.make_span_weight, self.cost_weight])
        
        candidate.fitness += load_penalty + risk_penalty + parallel_penalty

    def create_neighbour_solution(self, amount: int, change_prob: float, max_changes: int = None) -> Solution:
        """
        based on the current solution create a neighbour solution by randomly assign new team to the job

        the amount of changes depends on the change_prob
        
        total changes can be limited by setting max_changes
        """
        
        neighbours = []
        for i in range(amount):
            limit = max_changes if max_changes else len(self.jobs)
            state = []

            s: State
            for s in self.current.state:
                new_state = State(s.job, s.team)
                if random.random() < change_prob and limit > 0 :
                    selected_team = random.choice([t for t in self.teams if t.job_focus == s.job.job_type])
                    new_state.team = selected_team
                    limit -= 1
                                    
                state.append(new_state)
                        
            neighbour = Solution(state)
            neighbours.append(neighbour)
        
        return neighbours
    
    def decide_solution(self):
        """
        accepts the neighbour solution based on probability

        find the best neighbour and replace the current ones if the neighbour is better

        else use probability to decide to accept worse neighbour
        """
        best_neighbour = min(self.neighbours, key=lambda x: x.fitness)
        diff = best_neighbour.fitness - self.current.fitness
        # if the diff is negative, means that neighbour is better than current solution
        # always accept the solution when diff < 0
        # no need to evaluate when diff == 0
        if diff <= 0:
            self.current = best_neighbour
        else:
            # NOTE the diff must be positive number
            accept_prob = np.exp(-diff/self.temperature)
            if random.random() <= accept_prob:
                print("RNG god has choosen the worse solution")
                self.current = best_neighbour

    def cool_down(self):
        self.temperature *= self.cooling_rate
        # preventing temperature going too low
        self.temperature = max(self.temperature, 0.0001)

def run() -> Solution:
    jobs = config.jobs
    teams = config.teams

    anneal = Anneal(jobs, teams, cooling_rate=0.99, temperature=1000)
    anneal.current = anneal.create_initial_solution()
    anneal.evaluate_candidate(anneal.current)
    
    while anneal.iteration <= 800:
        print(f"iteration {anneal.iteration} | temp: {anneal.temperature}")
        anneal.neighbours = anneal.create_neighbour_solution(10, np.exp(-anneal.iteration/anneal.temperature), 1)
        for n in anneal.neighbours:
            anneal.evaluate_candidate(n)
        anneal.decide_solution()
        anneal.cool_down()

        if anneal.iteration == 1:
            anneal.best = anneal.current
            print(f"New best found! | {anneal.best.state}")
        else:
            if anneal.current.fitness < anneal.best.fitness:
                anneal.best = anneal.current
                anneal.best.selected = anneal.iteration
                print(f"New best found! | {anneal.best.state}")

        history = (
            np.mean([n.fitness for n in anneal.neighbours]),
            anneal.best.fitness,
            anneal.temperature
        )
        anneal.hist.append(history)

        anneal.iteration += 1
    
    fig, ax1 = plt.subplots()
    ax1.plot([h[0] for h in anneal.hist], color="g", label="Average fitness")
    ax1.plot([h[1] for h in anneal.hist], color="b", label="Best fitness")
    ax1.legend(loc="upper left")
    ax2 = ax1.twinx()
    ax2.plot([h[2] for h in anneal.hist], color="r", label="Temperature")
    ax2.legend(loc="upper right")
    plt.show()

    return anneal.best

solution = run()
helper.print_schedule(solution.state)
print(f"Solution job balance: {solution.load_balance}")
print(f"Solution risk balance: {solution.risk_balance}")
print(f"Solution parallel balance: {solution.parallel}")
print(f"Solution is selected at iteration {solution.selected}")
print(f"Solution string: {solution.state}")
