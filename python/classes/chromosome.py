import random

class Chromosome:
    # size: size of the chromosome
    # mutations: quantity of genes to be mutated
    # genes
    def __init__(self, size, gene_mutations=2, genes = []):
        self.size = size
        self.gene_mutations = gene_mutations
        self.genes = []

        # Populate the gen ensuring that the genes are unique.
        if genes is None or len(genes) == 0:
            while len(self.genes) != self.size:
                gen = random.randint(0, self.size - 1)
                if gen not in self.genes:
                    self.genes.append(gen)
        else:
            self.genes = genes

    def get_size(self):
        return self.size

    def get_gen(self, index):
        return self.genes[index]

    def get_genes(self):
        return self.genes

    # Mutate `gene_mutations` couple of genes.
    def perform_mutation(self, probability = 0.5):
        if self.size > 0:
            if random.uniform(0, 1) <= probability:
                for _ in range(self.gene_mutations):
                    # Get two random genes indexes
                    gen_to_mutate_a = random.randint(0, self.size - 1)
                    gen_to_mutate_b = random.randint(0, self.size - 1)

                    # Regenerate one of the gene indexes if both are the same one.
                    while gen_to_mutate_a == gen_to_mutate_b:
                        gen_to_mutate_a = random.randint(0, self.size - 1)

                    # Swap genes
                    self.genes[gen_to_mutate_a], self.genes[gen_to_mutate_b] = self.genes[gen_to_mutate_b], self.genes[gen_to_mutate_a]
    
    def json(self):
        return {
            'size': self.size,
            'gene_mutations': self.gene_mutations,
            'genes': self.genes
        }

    def __str__(self):
        return str(self.json())
                