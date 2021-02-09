import random
import sys
import time
import uuid

from .chromosome import Chromosome

VARIANTS = ['standard', 'lamarckian', 'baldwinian']

class Population:
    # Run time.
    run_time = 0

    # Number of chromosomes
    size = 0

    # Path where the data is stored
    database = ''

    # Flows and distances
    flows = []
    distances = []
    
    # Array of dictionaries.
    # Each dict contains:
    # { ch: chromosome, fitness: its fitness value }
    fitness = []
    
    def __init__(self,
        database,
        variant='standard',
        generations=100,
        mutation_probability=0.5,
        cross_probability=0.5,
        gene_mutations=2,
        best_chromosomes_ratio=0.1,
        seed=None
    ):
        # Algorithm iterations.
        self.iterations = 0

        self.variant = variant if variant in VARIANTS else 'regular'

        self.best_chromosome = { 'fitness': sys.maxsize }

        # Generations management.
        self.generations = generations

        # Database management + fetch data.
        self.database = database
        self.__fetch_data_from_database()

        # Mutation and cross probabilities.
        self.mutation_probability = mutation_probability
        self.cross_probability = cross_probability

        # Genes to be mutated
        self.gene_mutations = gene_mutations

        # Ratio of best elements to be taken in mind when reproducing
        self.best_chromosomes_ratio = best_chromosomes_ratio

        # Seed management.
        self.seed = uuid.uuid4() if seed is None else uuid.UUID(seed)
        random.seed(self.seed)

        # Generate first chromosomes.
        self.chromosomes = [Chromosome(size=self.size, gene_mutations=self.gene_mutations) for _ in range(self.size)]

    def __fetch_data_from_database(self):
        with open(self.database) as file:
            content = file.readlines()
            self.size = int(content[0].strip())

            for i in range(2, self.size + 2):
                line = content[i].strip().replace('\n', '')
                splitted = list(filter(None, line.split(' ')))
                self.flows.append([int(val.replace('\n', '')) for val in splitted])

            for i in range(self.size + 3, (self.size * 2) + 3):
                line = content[i].strip().replace('\n', '')
                splitted = list(filter(None, line.split(' ')))
                self.distances.append([int(val.replace('\n', '')) for val in splitted])

    def __compute_fitness_by_chromosome(self, chromosome):
        fitness = 0
        
        if self.variant == 'standard':
            for i in range(self.size):
                for j in range(self.size):
                    fitness += self.flows[i][j] * self.distances[chromosome.get_gen(i)][chromosome.get_gen(j)]
        
        elif self.variant == 'baldwinian':
            for i in range(self.size):
                checked_j = []
                for j in range(self.size):
                    best = self.__nearest_neighbour(chromosome.get_gen(i), checked_j)
                    checked_j.append(best)
                    fitness += self.flows[i][j] * self.distances[chromosome.get_gen(i)][best]

        return fitness

    def __nearest_neighbour(self, i, checked):
        row = self.distances[i]

        best = sys.maxsize
        bbest = sys.maxsize

        for j, value in enumerate(row):
            if j not in checked and value < best:
                best = j
                bbest = value

        # print(bbest, best, " ## ", row)
        return best
        

    def compute_all_chromosomes_fitness(self):
        # Compute the fitness of all chromosomes.
        fitness = [{
                'ch': ch,
                'fitness': self.__compute_fitness_by_chromosome(ch)
            } for ch in self.chromosomes]

        # Order the chromosomes by its fitness.
        self.fitness = sorted(fitness, key=lambda f: f['fitness'])

        return self.fitness

    def mutate_chromosomes(self):
        for ch in self.chromosomes:
            ch.perform_mutation(self.mutation_probability)

    def reproduce_chromosomes(self):
        if random.uniform(0, 1) < self.cross_probability:
            # Possible best chromosomes.
            pbc = self.size * self.best_chromosomes_ratio

            # Ensure that the possible best chromosomes are at least 2.
            pbc = int(pbc if pbc >= 2 else 2)

            # Array with the best chromosomes.
            best_chs = self.fitness[:pbc]

            # Add the first best chromosomes.
            children = [
                ch['ch'] for ch in best_chs
            ]

            for _ in range(self.size - pbc):
                # Random split point.
                split = random.randint(0, self.size - 1)

                # Get parents and join them.
                parents = random.sample(best_chs, 2)
                
                # Add first genes
                joined_genes = parents[0]['ch'].get_genes()[split:]
                
                genes_b = parents[0]['ch'].get_genes()[:split]

                for i in range(len(genes_b)):
                    if genes_b[i] not in joined_genes:
                        joined_genes.append(genes_b[i])
                    else:
                        r_gen = random.randint(0, self.size - 1)
                        while r_gen in genes_b or r_gen in genes_b:
                            r_gen = random.randint(0, self.size - 1)
                        
                        joined_genes.append(r_gen)

                # Child chromosome.
                child = Chromosome(
                    size=parents[0]['ch'].get_size(),
                    genes=joined_genes,
                    gene_mutations=self.gene_mutations
                )

                # Add new children.
                children.append(child)

                # Assign new chromosomes.
                self.chromosomes = children

    def compute_best_chromosome(self):
        best = sorted(self.fitness, key=lambda f: f['fitness'])[0]

        if best['fitness'] < self.best_chromosome['fitness']:
            self.best_chromosome = {
                'ch': best['ch'].get_genes(),
                'fitness': best['fitness'],
                'generation': self.iterations
            }

    def get_best_chromosome(self):
        return self.best_chromosome

    def run(self):
        start_time = time.time()

        for it in range(self.generations):
            # Increment iterations.
            self.iterations += 1

            # If the variant 
            if self.variant == 'lamarckian':
                continue

            # Compute algorithm.
            self.compute_all_chromosomes_fitness()
            self.reproduce_chromosomes()
            self.mutate_chromosomes()

            # If last iteration, compute the final fitness.
            if it == self.generations - 1:                
                self.compute_all_chromosomes_fitness()

            # Update the best chromosome.
            self.compute_best_chromosome()

        self.run_time = round(time.time() - start_time, 2)

    def greedy_transposition(self, chromosome):
        current_genes = chromosome.get_genes()

        while True:
            best = current_genes
            for i in range(self.size):
                for j in range(i + 1, self.size, 1):
                    copy = current_genes
                    copy[i], copy[j] = copy[j], copy[i]

                    # Compute the fitness for the transposited chromosome.
                    transposition_fitnes = self.__compute_fitness_by_chromosome(
                        Chromosome(size=self.size, gene_mutations=self.gene_mutations, genes=copy)
                    )
                    
                    # Compute the fitness for the current chromosome.
                    transposition_current_genes = self.__compute_fitness_by_chromosome(
                        Chromosome(size=self.size, gene_mutations=self.gene_mutations, genes=current_genes)
                    )

                    # Update the current genes if the transposition fitness is lower than the current one.
                    # This means that the transposited chromosome is better.
                    if transposition_current_genes < transposition_fitnes:
                        current_genes = copy

            if best == current_genes:
                break

    ########################################################################

    def json(self):
        return {
            'database': self.database,
            'variant': self.variant,
            'population_size': self.size,
            'mutation_probability': self.mutation_probability,
            'cross_probability': self.cross_probability,
            'generations': self.generations,
            'seed': str(self.seed),
            'run_time': self.run_time,
            # 'chromosomes': [ ch.get_genes() for ch in self.chromosomes ],
            # 'fitness': [ f['fitness'] for f in self.fitness ],
            'best_chromosome': self.get_best_chromosome()
        }

    def __str__(self):
        return str(self.json())

