from models.assignment import Assignment
from models.job import Job
from models.team import Team
from helpers import helper
import random
import numpy as np
from matplotlib import pyplot as plt
import config

class Path(Assignment):
    """
    represent a possible path that can be taken by the ant

    path is initialized with high pheromone to encourage exploration
    """
    def __init__(self, j: Job, t: Team) -> None:
        super().__init__(j, t)
        self.pheromone = 1

class Ant:
    """
    represent an ant in the colony
    """
    def __init__(self) -> None:
        self.path_taken = []
        
        self.make_span = 0
        self.cost = 0
        self.load_balance = 0
        self.risk_balance = 0
        self.parallel = 0
        self.fitness = 0

        self.selected = 1

    def explore(self, paths: list, jobs: list) -> None:
        """
        select a path from the list of paths as a possible solution

        the chance of selecting a path depends on the pheromone level
        """
        path = []
        for j in jobs:
            valid_path = [p for p in paths if p.job == j]
            path_weight = [p.pheromone for p in valid_path]
            choosen_path = random.choices(valid_path, path_weight)[0]
            path.append(choosen_path)
        
        self.path_taken = path

    def leave_pheromone(self) -> None:
        """
        leave pheromones on the path depending on the fitness of the solution
        """
        pheromone = 1 / self.fitness
        p:Path
        for p in self.path_taken:
            p.pheromone += pheromone

class AntColony:
    def __init__(self, population: int, evaporate: float, jobs: list, teams: list, make_span_weight: float = 0.5, cost_weight: float = 0.5) -> None:
        self.jobs= jobs
        self.teams = teams
        self.job_topo_order = helper.kahn_sort(self.jobs)

        self.iteration = 1
        
        self.make_span_weight = make_span_weight
        self.cost_weight = cost_weight

        # the amount pheromone left after each iteration
        self.p_left = 1 - evaporate

        # all the possible paths that can be taken by the ants
        self.paths = []
        self.initialize_path_matrix()
        # the ant in the colony
        self.population = population
        self.ants = [Ant() for i in range(self.population)]

        self.best:Ant = None

        self.hist = []
    
    def initialize_path_matrix(self) -> None:
        """
        initialize the job team matrix
        """
        for j in self.jobs:
            for t in self.teams:
                if j.job_type == t.job_focus:
                    path = Path(j, t)
                    self.paths.append(path)

    def evaluate_ant(self, ant: Ant) -> None:
        """
        evaluates the fitness of the solution found by the ant
        """
        make_span = helper.calculate_make_span(ant.path_taken, self.job_topo_order)
        ant.make_span = make_span
        
        cost = helper.calculate_cost(ant.path_taken, self.teams)
        ant.cost = cost

        load_penalty = helper.calculate_distribution_penalty(ant.path_taken, self.jobs, self.teams)
        ant.load_balance = load_penalty

        risk_penalty = helper.calculate_risk_penalty(ant.path_taken, self.teams)
        ant.risk_balance = risk_penalty

        parallel_penalty = helper.calculate_parallel_penalty(ant.path_taken, self.teams, self.job_topo_order)
        ant.parallel = parallel_penalty

        ant.fitness = self.make_span_weight * make_span + self.cost_weight * cost
        ant.fitness /= sum([self.make_span_weight, self.cost_weight])
        
        ant.fitness += load_penalty + risk_penalty + parallel_penalty
    
    def update_pheromone(self) -> None:
        """
        updates the pheromone
        """
        # evaporates the pheromone
        p: Path
        for p in self.paths:
            p.pheromone *= self.p_left
        
        # ants leaving pheromone
        for a in self.ants:
            a.leave_pheromone()
        

def run() -> Ant:
    ant_colony = AntColony(10, 0.1, config.jobs, config.teams)

    while ant_colony.iteration <= 800:
        print(f"Iteration {ant_colony.iteration}")
        
        a: Ant
        for a in ant_colony.ants:
            if a != ant_colony.best:
                a.explore(ant_colony.paths, ant_colony.jobs)
                ant_colony.evaluate_ant(a)
        
        ant_colony.update_pheromone()
        
        # finding the best for each iteration
        best = min(ant_colony.ants, key=lambda x: x.fitness)
        if ant_colony.iteration == 1:
            ant_colony.best = best
            print(f"new best found | {ant_colony.best.path_taken}")
        else:
            if best.fitness < ant_colony.best.fitness:
                ant_colony.best = best
                ant_colony.best.selected = ant_colony.iteration
                print(f"new best found | {ant_colony.best.path_taken}")

        history = (
           np.mean([a.fitness for a in ant_colony.ants]),
           ant_colony.best.fitness,
           np.mean([p.pheromone for p in ant_colony.paths]),
           np.mean([p.pheromone for p in ant_colony.best.path_taken]),
        )
        ant_colony.hist.append(history)

        ant_colony.iteration += 1
    
    fig, ax1 = plt.subplots()
    ax1.plot([h[0] for h in ant_colony.hist], color="g", label="Average fitness")
    ax1.plot([h[1] for h in ant_colony.hist], color="b", label="Best fitness")
    ax1.legend(loc="upper left")
    ax2 = ax1.twinx()
    ax2.plot([h[2] for h in ant_colony.hist], color="r", label="Average pheromones")
    ax2.plot([h[3] for h in ant_colony.hist], color="m", label="Best pheromones")
    ax2.legend(loc="upper right")
    plt.show()

    return ant_colony.best

solution = run()
helper.print_schedule(solution.path_taken)
print(f"Solution job balance: {solution.load_balance}")
print(f"Solution risk balance: {solution.risk_balance}")
print(f"Solution parallel balance: {solution.parallel}")
print(f"Solution is selected at iteration {solution.selected}")
print(f"Solution string: {solution.path_taken}")

