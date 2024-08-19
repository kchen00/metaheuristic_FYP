from models.assignment import Assignment
from models.job import Job
from models.team import Team
from helpers import helper
import random
import numpy as np
from matplotlib import pyplot as plt

random.seed(1)

class Gene(Assignment):
    def __init__(self, j: Job, t: Team) -> None:
        super().__init__(j, t)

class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes = genes
        self.fitness = 0
        self.make_span = 0
        self.cost = 0
        
        # how balance is the job distribution
        self.load_balance = 0
        # how balance if the job risk distribution
        self.risk_balance = 0
        
        self.selected = 1
    
    def cross_over(self, partner: 'Chromosome') -> 'Chromosome':
        """
        produce new chromosome using a single point cross over
        """

        # some assert check to make sure that all things are correct
        # making sure that the length of genes are the same
        assert len(self.genes) == len(partner.genes)
        for s, p in zip(self.genes, partner.genes):
            # make sure the job object is the same
            assert s.job == p.job, f"{s.job.name} is not {p.job.name}"
        
        # choosing a random point for cross over
        random_point = random.randint(1, len(self.genes) - 1)

        # slicing genes from self and partner
        upper_gene = self.genes[:random_point]
        lower_gene = partner.genes[random_point:]
        comb_gene = upper_gene + lower_gene

        # extracting the job and team from original genes
        # create a new gene object from it
        bebe_gene = []
        g: Gene
        for g in comb_gene:
            new_gene = Gene(g.job, g.team)
            bebe_gene.append(new_gene)

        # some assertion check again to make sure things are correct
        for s, b in zip(self.genes, bebe_gene):
            assert s.job == b.job

        bebe = Chromosome(bebe_gene)
        return bebe

class Population:
    def __init__(self, jobs: list, teams: list, size: int, cross_over_rate: float = 0.95, mutation_rate: float = 0.1, make_span_weight: float = 0.5, cost_weight: float = 0.5):
        """
        represent a population of chromosome
        
        use high cross over rate, and low mutation rate
        """
        self.generation = 1
        self.size = size
        self.chromosomes = []

        # list of teams and jobs
        self.jobs = jobs
        self.teams = teams
        
        # weights on what to prioritize
        self.make_span_weight = make_span_weight
        self.cost_weight = cost_weight

        self.cross_over_rate = cross_over_rate
        self.mutation_rate = mutation_rate

        self.previous_high = 0
        self.previous_low = 0
        # storing the best solution
        self.best = None

        self.hist = []

    def generate_chromosomes(self, amount: int):
        """
        generate chromosomes based on the amount specified
        """
        for i in range(amount):
            genes = []
            j: Job
            for j in self.jobs:
                choosen_team = random.choice([t for t in self.teams if t.job_focus == j.job_type])
                new_gene = Gene(j, choosen_team)
                genes.append(new_gene)

            new_chromosome = Chromosome(genes)
            self.chromosomes.append(new_chromosome)
        

    def evaluate_chromosome(self):
        """
        evaluates the fitness of the chromosome
        """
        c: Chromosome
        for c in self.chromosomes:
            # fitness in terms of make span
            make_span_t, make_span = helper.calculate_make_span(c.genes)
            c.make_span = make_span
            # fitness in terms of cost
            cost_t, cost = helper.calculate_cost(c.genes)
            c.cost = cost
            
            # penalty in terms of task distribution
            load_penalty = helper.calculate_distribution_penalty(c.genes, self.jobs, self.teams)
            c.load_balance = load_penalty
            
            risk_penalty = helper.calculate_risk_penalty(c.genes, self.teams)
            c.risk_balance = risk_penalty
            
            c.fitness = self.make_span_weight * make_span + self.cost_weight * cost
            c.fitness /= sum([self.make_span_weight, self.cost_weight])
            
            # adding penalty to final fitness because we minimizing the fitness
            c.fitness += load_penalty + risk_penalty

        current_best = min(self.chromosomes, key=lambda x: x.fitness)
        
        if self.generation == 1:
            self.best = current_best
            print(f"New best found! | {current_best.genes}")
        else:
            if current_best.fitness < self.best.fitness:
                self.best = current_best     
                self.best.selected = self.generation         
                print(f"New best found! | {current_best.genes}")
        
        self.hist.append(np.mean([c.fitness for c in self.chromosomes]))

    def rank_select(self, amount: int) -> list:
        """
        rank based selection
        
        sort the chromosome based on the rank and return the top percent chromosome specified
        """        
        # sort the chromosome based on the fitness
        self.chromosomes.sort(key=lambda x: x.fitness)
        # selecting the top percent of chromosome
        winners = self.chromosomes[:amount]
        print(f"Selected {len(winners)} chromosome in rank selection")
        return winners

    def tournament_select(self, amount: int) -> list:
        """
        tournament selection

        return a list chromomsome that wins the tournament according to amount specified
        """
        winners = []
        while len(winners) < amount and len(self.chromosomes) > 0:
            competitor = random.sample(self.chromosomes, 2)
            winner = competitor[0] if competitor[0].fitness < competitor[1].fitness else competitor[1]
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

        while len(winners) < amount and len(self.chromosomes) > 0:
            total_fitness = np.sum([c.fitness for c in self.chromosomes])
            cumulative_fit = 0
            random_fit = random.random()
            
            for c in self.chromosomes:
                cumulative_fit += c.fitness / total_fitness
                if random_fit <= cumulative_fit:
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

        while len(bebes) < bebes_to_produce:
            parents = random.sample(self.chromosomes, 2)
            for p1, p2 in [parents]:
                if random.random() < self.cross_over_rate:
                    bebe_1 = p1.cross_over(p2)
                    bebe_2 = p2.cross_over(p1)
                    bebes += [bebe_1, bebe_2]

        # mutate the genes in the bebe
        b: Chromosome
        for b in bebes:
            g: Gene
            for g in b.genes:
                if random.random() < self.mutation_rate:
                    g.team = random.choice([t for t in self.teams if t.job_focus == g.job.job_type])

        self.chromosomes += bebes

        # check if the population is less than the population size stated
        # else sample the population size needed only
        if len(self.chromosomes) > self.size:
            self.chromosomes = random.sample(self.chromosomes, self.size)

def run() -> Chromosome:
    jobs = helper.create_random_jobs(10)
    teams = helper.create_random_team(5)
    population = Population(jobs, teams, 400, cross_over_rate=0.98, mutation_rate=0.3)
    population.generate_chromosomes(population.size)
    
    while population.generation <= 800:
        print(f"Generation {population.generation} | population: {len(population.chromosomes)}")
        population.evaluate_chromosome()
        population.chromosomes = population.rank_select(250)
        population.produce_bebe()
        population.generation += 1

    plt.plot(population.hist)
    plt.show()

    return population.best

solution = run()
helper.print_schedule(solution.genes)
print(f"Solution job balance: {solution.load_balance}")
print(f"Solution risk balance: {solution.risk_balance}")
print(f"Solution is selected at generation {solution.selected}")
print(f"Solution string {solution.genes}")