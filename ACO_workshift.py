from models.assignment import Assignment
from models.job import Job
from models.employee import Employee
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
    def __init__(self, j: Job, e: Employee) -> None:
        super().__init__(j, e)
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
        self.risk_rank_ratio = 0

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
    def __init__(self, population: int, evaporate: float, jobs: list, employees: list) -> None:
        self.jobs= jobs
        self.employees = employees
        self.job_topo_order = helper.kahn_sort(self.jobs)

        self.iteration = 1
        
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
            for e in self.employees:
                if j.job_type == e.job_focus:
                    path = Path(j, e)
                    self.paths.append(path)

    def evaluate_ant(self, ant: Ant) -> None:
        """
        evaluates the fitness of the solution found by the ant
        """
        make_span = helper.calculate_make_span(ant.path_taken, self.job_topo_order)
        ant.make_span = make_span
        make_span *= config.make_span_op
        
        cost = helper.calculate_cost(ant.path_taken, self.employees)
        ant.cost = cost
        cost *= config.cost_op

        load_penalty = helper.calculate_distribution_penalty(ant.path_taken, self.jobs, self.employees)
        ant.load_balance = load_penalty

        risk_penalty = helper.calculate_risk_penalty(ant.path_taken, self.employees)
        ant.risk_balance = risk_penalty

        parallel_penalty = helper.calculate_parallel_penalty(ant.path_taken, self.employees, self.job_topo_order)
        ant.parallel = parallel_penalty

        job_risk_rank_penalty = helper.calculate_risk_rank_ratio_penalty(ant.path_taken, self.employees)
        ant.risk_rank_ratio = job_risk_rank_penalty

        ant.fitness = (make_span + cost) / config.total_weights_op
        ant.fitness += load_penalty + risk_penalty + parallel_penalty + job_risk_rank_penalty
    
    def update_pheromone(self, top: int = 0) -> None:
        """
        updates the pheromone

        set top to enable rank update, only the top ranking ants are choosen to update the pheromone
        """
        # evaporates the pheromone
        p: Path
        for p in self.paths:
            p.pheromone *= self.p_left
        
        # ants leaving pheromone
        if top > 0:
            self.ants.sort(key=lambda x: x.fitness)
            for a in self.ants[:top]:
                a.leave_pheromone()
        else:
            for a in self.ants:
                a.leave_pheromone()

        

def run() -> Ant:
    ant_colony = AntColony(10, 0.1, config.jobs, config.employees)

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
helper.print_formation(solution.path_taken)
print(f"Solution job balance: {solution.load_balance}")
print(f"Solution risk balance: {solution.risk_balance}")
print(f"Solution parallel balance: {solution.parallel}")
print(f"Solution risk rank ratio: {solution.risk_rank_ratio}")
print(f"Solution is selected at iteration {solution.selected}")
print(f"Solution string: {solution.path_taken}")
print(f"Seed: {config.seed}")