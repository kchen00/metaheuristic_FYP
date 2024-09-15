from models.assignment import Assignment
from models.job import Job
from models.employee import Employee
from helpers import helper
import random
import numpy as np
from matplotlib import pyplot as plt
import config

class Gene(Assignment):
    def __init__(self, j: Job, e: Employee) -> None:
        super().__init__(j, e)

class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes = genes
        self.fitness = 0
        self.make_span = 0
        self.cost = 0
        
        # how balance is the job distribution
        self.load_balance = 0
        # how balance of the job risk distribution
        self.risk_balance = 0
        # how parallel if the job distribution
        self.parallel = 0

        self.selected = 1
    
    def cross_over(self, partner: 'Chromosome') -> tuple:
        """
        produce two new chromosome using a single point cross over

        returns the two new chomosome produced
        """
        random_point = random.randint(1, len(self.genes) - 1)

        # genes for 1st bebe
        u1 = self.genes[:random_point]
        l1 = partner.genes[random_point:]
        
        # gene for 2nd bebe
        u2 = partner.genes[:random_point]
        l2 = self.genes[random_point:]

        b1_gene = u1 + l1
        b2_gene = u2 + l2

        b1 = Chromosome(b1_gene)
        b2 = Chromosome(b2_gene)

        return b1, b2

class Population:
    def __init__(self, jobs: list, employees: list, size: int, cross_over_rate: float = 0.95, mutation_rate: float = 0.1):
        """
        represent a population of chromosome
        
        use high cross over rate, and low mutation rate
        """
        self.generation = 1
        self.size = size
        self.chromosomes = []

        # list of teams and jobs
        self.jobs = jobs
        self.employees = employees
        self.job_topo_order = helper.kahn_sort(self.jobs)
        
        # gnerate all possible genes during start
        self.all_possible_genes = []
        self.generate_all_possible_gene()

        # generate inital population during start
        self.generate_chromosomes(self.size)

        self.cross_over_rate = cross_over_rate
        self.mutation_rate = mutation_rate

        # storing the best solution
        self.best = None

        self.hist = []

    def generate_all_possible_gene(self):
        """
        generate all possible genes during initiation
        """
        j: Job
        e: Employee
        for j in self.jobs:
            for e in self.employees:
                if j.job_type == e.job_focus:
                    gene = Gene(j, e)
                    self.all_possible_genes.append(gene)

    def generate_chromosomes(self, amount: int):
        """
        generate chromosomes based on the amount specified
        """
        for i in range(amount):
            choosen_genes = []
            for j in self.jobs:
                gene = random.choice([g for g in self.all_possible_genes if g.job == j])
                choosen_genes.append(gene)
            
            chromosome = Chromosome(choosen_genes)
            self.chromosomes.append(chromosome)

    def evaluate_chromosome(self, chromosome: Chromosome):
        """
        evaluates the fitness of the chromosome
        
        NOTE:  STRICLY FOR EVALUATING FITNESS
        """
        # fitness in terms of make span
        make_span = helper.calculate_make_span(chromosome.genes, self.job_topo_order)
        chromosome.make_span = make_span
        make_span *= config.make_span_op
        
        # fitness in terms of cost
        cost = helper.calculate_cost(chromosome.genes, self.employees)
        chromosome.cost = cost
        cost *= config.cost_op
        
        # penalty in terms of task distribution
        load_penalty = helper.calculate_distribution_penalty(chromosome.genes, self.jobs, self.employees)
        chromosome.load_balance = load_penalty
        
        risk_penalty = helper.calculate_risk_penalty(chromosome.genes, self.employees)
        chromosome.risk_balance = risk_penalty

        parallel_penalty = helper.calculate_parallel_penalty(chromosome.genes, self.employees, self.job_topo_order)
        chromosome.parallel = parallel_penalty
        
        chromosome.fitness = (make_span + cost) / config.total_weights_op
        # adding penalty to final fitness because we minimizing the fitness
        chromosome.fitness += load_penalty + risk_penalty + parallel_penalty

    def rank_select(self, amount: int) -> list:
        """
        rank based selection
        
        sort the chromosome based on the rank and return the top chromosome specified
        """        
        # sort the chromosome based on the fitness
        # since lower fitness is better, sorting needs to be ascending
        self.chromosomes.sort(key=lambda x: x.fitness)
        
        # selecting the top chromosome
        winners = self.chromosomes[:amount]
        print(f"Selected {len(winners)} chromosome in rank selection")
        
        return winners

    def tournament_select(self, amount: int) -> list:
        """
        tournament selection

        return a list chromomsome that wins the tournament according to amount specified
        """
        winners = []
        for i in range(amount):
            competitor = random.sample(self.chromosomes, 2)
            winner = None
            c1: Chromosome = competitor[0]
            c2: Chromosome = competitor[1]

            # when both chromosome is equally good, random select one of them
            if c1.fitness == c2.fitness:
                winner = random.choice(competitor)
            # since the fitness is better when lower, winner is the one that have the lower fitness
            else:
                winner = c1 if c1.fitness < c2.fitness else c2
            
            winners.append(winner)
            # remove the winner from the population so that it is not selected again
            self.chromosomes.remove(winner)
        
        print(f"Selected {len(winners)} chromosome in tournament selection")
        return winners
    
    def roulette_selection(self, amount: int) -> list:
        """
        roulette selection

        return a list of selected chromosome based on the amount specified
        """
        winners = []
        
        for i in range(amount):
            sum_of_fitness = sum([1/c.fitness for c in self.chromosomes])
            cumulative_fit = 0
            random_fit = random.random()

            c: Chromosome
            for c in self.chromosomes:
                cumulative_fit += (1/c.fitness) / sum_of_fitness
                if cumulative_fit >= random_fit:
                    winners.append(c)
                    self.chromosomes.remove(c)
                    break

        print(f"Selected {len(winners)} chromosome in roulette selection")
        return winners

    def produce_bebe(self):
        """
        cross over operation to produce new bebe
        
        then randomly mutate the gene of the bebe produced

        produce bebe until population is equal to population size
        """
        bebes = []
        bebes_to_produce = self.size - len(self.chromosomes)

        # choose two parent then let RNG god to decide whether or not to produce bebe
        while bebes_to_produce > 0:
            parents = random.sample(self.chromosomes, 2)
            if random.random() < self.cross_over_rate:
                p1: Chromosome = parents[0]
                p2: Chromosome = parents[1]
                
                bebe_1, bebe_2 = p1.cross_over(p2)


                bebes.append(bebe_1)
                bebes.append(bebe_2)

                bebes_to_produce -= 2

        # after the bebes is produced, do random mutations
        b: Chromosome
        for b in bebes:
            for i in range(len(b.genes)):
                if random.random() < self.mutation_rate:
                    mutated_gene = [g for g in self.all_possible_genes if g != b.genes[i] and g.job == b.genes[i].job]
                    choosen_mutation = random.choice(mutated_gene)
                    b.genes[i] = choosen_mutation
        
        self.chromosomes += bebes
        print(f"Produced {len(bebes)} bebes in generation {self.generation}")

def run() -> Chromosome:
    jobs = config.jobs
    employees = config.employees
    population = Population(jobs, employees, 400, cross_over_rate=0.98, mutation_rate=0.1)
    
    while population.generation <= 400:
        for c in population.chromosomes:
            population.evaluate_chromosome(c)

        current_best = min(population.chromosomes, key=lambda x: x.fitness)
        if population.generation == 1:
            population.best = current_best
            print(f"New best found! | {current_best.genes}")
        else:
            if current_best.fitness < population.best.fitness:
                population.best = current_best     
                population.best.selected = population.generation         
                print(f"New best found! | {current_best.genes}")
        
        history = (
            np.mean([c.fitness for c in population.chromosomes]),
            population.best.fitness
        )
        population.hist.append(history)
        
        # eliminating chromosome
        population.chromosomes = population.rank_select(250)
        # produce the next generatin
        population.produce_bebe()

        population.generation += 1
    
    fig, ax1 = plt.subplots()
    ax1.plot([h[0] for h in population.hist], color="g", label="Average fitness")
    ax1.plot([h[1] for h in population.hist], color="b", label="Best fitness")
    ax1.legend(loc="upper right")
    plt.show()

    return population.best

solution = run()
helper.print_formation(solution.genes)
print(f"Solution job balance: {solution.load_balance}")
print(f"Solution risk balance: {solution.risk_balance}")
print(f"Solution parallel balance: {solution.parallel}")
print(f"Solution is selected at generation {solution.selected}")
print(f"Solution string {solution.genes}")
print(f"Seed: {config.seed}")