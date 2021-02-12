import java.util.ArrayList;
import static java.util.Collections.shuffle;

public class Chromosome {
    private Integer size;
    private Integer gene_mutations;
    private ArrayList<Integer> genes = new ArrayList<>();

    public Chromosome(Integer size, Integer gene_mutations, ArrayList<Integer> genes) {
        this.size = size;
        this.gene_mutations = gene_mutations;

        if (genes == null || genes.size() == 0) {
            for (int i =0; i < this.size; ++i) {
                this.genes.add(i);
            }

            shuffle(this.genes, Main.random);
        } else {
            this.genes = genes;
        }
    }

    public ArrayList<Integer> getGenes() {
        return this.genes;
    }

    public Integer getGen(Integer index) {
        return this.genes.get(index);
    }

    public Integer getSize() {
        return this.size;
    }

    public void performMutation(double probability) {
        if (Main.random.nextDouble() < probability) {
            for (int i = 0; i < this.gene_mutations; ++i) {
                Integer genToMutateA = Main.random.nextInt(this.size);
                Integer genToMutateB = Main.random.nextInt(this.size);

                while(genToMutateA == genToMutateB) {
                    genToMutateA = Main.random.nextInt(this.size);
                }

                Integer aux = this.genes.get(genToMutateA);
                this.genes.set(genToMutateA, this.genes.get(genToMutateB));
                this.genes.set(genToMutateB, aux);
            }
        }
    }

    @Override
    public String toString() {
        return "Chromosome{" +
                "genes=" + genes +
                '}';
    }
}
