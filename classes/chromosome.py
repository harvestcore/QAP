import random

class Chromosome:
    # size: size of the chromosome
    # mutations: quantity of genes to be mutated
    # genes
    def __init__(self, size, gene_mutations=2, genes = []):
        self.size = size
        self.gene_mutations = gene_mutations
            
        self.genes = []

        if genes is None or len(genes) == 0:
            for _ in range(self.size):
                self.genes.append(random.randint(0, self.size - 1))
        else:
            self.genes = genes

    def get_size(self):
        return self.size

    def get_gen(self, index):
        return self.genes[index]

    def get_genes(self):
        return self.genes

    def perform_mutation(self, probability = 0.5):
        if self.size > 0:
            prob = random.uniform(0, 1)

            if prob <= probability:
                for _ in range(self.gene_mutations):
                    gen_to_mutate = random.randint(0, self.size - 1)
                    mutatation = random.randint(0, self.size - 1)

                    while mutatation == self.genes[gen_to_mutate]:
                        mutatation = random.randint(0, self.size - 1)

                    self.genes[gen_to_mutate] = mutatation
    
    def json(self):
        return {
            'seed': self.seed,
            'genes': self.genes
        }

    def __str__(self):
        return str(self.json())
                