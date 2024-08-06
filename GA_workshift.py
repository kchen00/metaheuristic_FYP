from models.assignment import Assignment
from models.job import Job
from models.team import Team
from helpers import helper
import random
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt

class Gene(Assignment):
    def __init__(self, j: Job, t: Team) -> None:
        super().__init__(j, t)

class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes = genes
        self.fitness = 0
    
    def cross_over(self, partner: 'Chromosome') -> 'Chromosome':
        """
        produce new chromosome using a single point cross over
        """
        # assert len(self.genes) == len(partner.genes)
        # for s, p in zip(self.genes, partner.genes):
        #     assert s.job == p.job, f"{s.job.name} is not {p.job.name}"
        
        random_point = random.randint(1, len(self.genes) - 1)

        # slicing genes from self and partner
        upper_gene = self.genes[:random_point]
        lower_gene = partner.genes[random_point:]

        bebe_gene = upper_gene + lower_gene
        # assert len(bebe_gene) == len(self.genes)

        # handling case where one job has 2 team assigned
        unique_jobs = {g.job for g in bebe_gene}

        for j in unique_jobs:
            extra_genes = {g for g in bebe_gene if g.job == j and g.active}
            
            if len(extra_genes) > 1:
                for g in extra_genes:
                    g.active = False

                best_gene = min(extra_genes, key=lambda x: x.make_span)
                best_gene.active = True
        
        # assert len([g for g in bebe_gene if g.active]) == len(unique_jobs), f"bebe gene has {len([g for g in bebe_gene if g.active])} active genes, but {len(unique_jobs)} is needed"


        bebe = Chromosome(bebe_gene)
        return bebe

class Population:
    def __init__(self, size: int, top: float = 0.5, cross_over_rate: float = 0.95, mutation_rate: float = 0.1):
        """
        represent a population of chromosome
        
        use high cross over rate, and low mutation rate
        """
        self.generation = 1
        self.size = size
        self.chromosomes = []
        
        self.top = top
        self.cross_over_rate = cross_over_rate
        self.mutation_rate = mutation_rate

        self.hist = []

    def generate_chromosomes(self, amount: int, jobs: list, teams: list):
        """
        generate chromosomes based on the amount specified
        """
        genes = []
        for j in jobs:
            for t in teams:
                new_gene = Gene(j, t)
                genes.append(new_gene)

        for i in range(amount):
            new_chromosome = Chromosome(genes)

            unique_jobs = {g.job for g in new_chromosome.genes}
            for j in unique_jobs:
                # given a job, choose a random gene to be activated
                choosen_gene = random.choice([g for g in new_chromosome.genes if g.job == j])
                choosen_gene.active = True

            self.chromosomes.append(new_chromosome)


    def evaluate_chromosome(self):
        """
        evaluates the fitness of the chromosome
        """
        c: Chromosome
        for c in self.chromosomes:
            t, c.fitness = helper.calculate_make_span(c.genes)
        
    
    def eliminate_chromosome(self):
        """
        eliminates chromosomes that are unfit, selecting the top min_fit% of the chromosome
        """
        before = len(self.chromosomes)
        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)
        top = int(before * self.top)
        self.chromosomes = self.chromosomes[top:]

        after = len(self.chromosomes)

        self.hist.append(np.mean([c.fitness for c in self.chromosomes]))
        
        print(f"eliminated {before-after} chromosome")
    
    def tournament(self, p1:Chromosome, p2:Chromosome):
        return p1 if p1.fitness > p2.fitness else p2

    def produce_bebe(self, amount: int):
        """
        cross over operation using tournament selection
        
        then randomly mutate the gene produced
        """

        bebes = []
        if random.random() < self.cross_over_rate:
            for i in range(amount):
                competitors = random.sample(self.chromosomes, 4)
                random.shuffle(competitors)

                p1 = self.tournament(competitors[0], competitors[1])
                p2 = self.tournament(competitors[2], competitors[3])

                bebe_1 = p1.cross_over(p2)
                bebe_2 = p2.cross_over(p1)

                bebes += [bebe_1, bebe_2]

        # mutate the genes in the bebe
        for b in bebes:
            unique_jobs = {g.job for g in b.genes}

            for j in unique_jobs:
                if random.random() < self.mutation_rate:
                    genes = [g for g in b.genes if g.job == j]

                    for g in genes:
                        g.active = False
                    
                    selected_gene = random.choice(genes)
                    selected_gene.active = True

        self.chromosomes += bebes

        # check if the population is less than the population size stated
        # else sample the population size needed only
        if len(self.chromosomes) > self.size:
            self.chromosomes = random.sample(self.chromosomes, self.size)
        else:
            # just produce some copy of existing chromosome to make up the number of chromosome
            while len(self.chromosomes) < self.size:
                random_chromosome = random.choice(self.chromosomes)
                new_chromosome = Chromosome(random_chromosome.genes)
                self.chromosomes.append(new_chromosome)


jobs = helper.create_random_jobs(10)
teams = helper.create_random_team(5)

def run() -> Chromosome:
    population = Population(500, cross_over_rate=0.8, mutation_rate=0.1)
    population.generate_chromosomes(population.size, jobs, teams)
    
    while population.generation <= 100:
        print(f"Generation {population.generation}")
        population.evaluate_chromosome()
        population.eliminate_chromosome()
        population.produce_bebe(int(population.size*0.2))
        population.generation += 1
    
    solution = min(population.chromosomes, key=lambda x: x.fitness)

    plt.plot(population.hist)
    plt.show()

    return solution

