import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Population {
    private double runTime = 0.0;
    private Integer iterations = 0;
    private Integer size = 0;
    private Integer generations;
    private String database;

    private ArrayList<Chromosome> chromosomes;
    private ArrayList<Integer> flows;
    private ArrayList<Integer> distances;
    private ArrayList<ChValue> fitness;

    private ChValue bestChromosome;

    private Integer populationSize;
    private Variant variant;
    private Double mutationProbability;
    private Double crossProbability;
    private Integer geneMutations;
    private Double bestChromosomesRatio;

    private UUID seed;

    public Population(String database, Integer populationSize, Integer generations, Variant variant, Double mutationProbability, Double crossProbability, Integer geneMutations, Double bestChromosomesRatio, UUID seed) {
        this.database = database;
        this.generations = generations;
        this.populationSize = populationSize;
        this.variant = variant;
        this.mutationProbability = mutationProbability;
        this.crossProbability = crossProbability;
        this.geneMutations = geneMutations;
        this.bestChromosomesRatio = bestChromosomesRatio;
        this.seed = seed;

        this.fetchDataFromDatabase();

        this.bestChromosome = new ChValue();

        this.chromosomes = new ArrayList<>();

        for (int i = 0; i < this.populationSize; ++i)
            this.chromosomes.add(new Chromosome(this.size, this.geneMutations, null));
    }

    private void fetchDataFromDatabase() {
        try (Scanner scanner = new Scanner(new File(this.database))) {
            this.size = scanner.nextInt();

            this.flows = new ArrayList<>();
            this.distances = new ArrayList<>();

            for (int i = 0; i < this.size; ++i) {
                for (int j = 0; j < this.size; ++j) {
                    Integer item = scanner.nextInt();
                    this.flows.add(item);
                }
            }

            for (int i = 0; i < this.size; ++i) {
                for (int j = 0; j < this.size; ++j) {
                    Integer item = scanner.nextInt();
                    this.distances.add(item);
                }
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    private Integer computeFitnessByChromosome(Chromosome ch) {
        Integer fitness = 0;

//        List fit = Collections.synchronizedList(new ArrayList<Integer>());
//
//        IntStream.range(0, this.size).parallel().forEach(i -> {
//            IntStream.range(0, this.size).parallel().forEach(j -> {
//                fit.add(this.flows.get(this.size * i + j) * this.distances.get(this.size * ch.getGen(i) + ch.getGen(j)));
//            });
//        });
//
//        return fit.stream().mapToInt(i -> (int) i).sum();

        for (int i = 0; i < this.size; ++i)
            for (int j = 0; j < this.size; ++j)
                fitness += this.flows.get(this.size * i + j) * this.distances.get(this.size * ch.getGen(i) + ch.getGen(j));

        return fitness;
    }

    public void computeAllChromosomesFitness() {
        this.fitness = new ArrayList<>();


        for (int i = 0; i < this.chromosomes.size(); ++i) {
            Chromosome ch = this.chromosomes.get(i);
            Integer fitnessToBeSet = 0;
            if (this.variant == Variant.BALDWINIAN) {
                Chromosome copy = this.greedyTransposition(ch);
                fitnessToBeSet = this.computeFitnessByChromosome(copy);
            } else {
                fitnessToBeSet = this.computeFitnessByChromosome(ch);
            }

            this.fitness.add(new ChValue(ch, fitnessToBeSet));
        }

        this.fitness.sort(Comparator.comparingInt((ChValue o) -> o.fitness));
    }

    public void mutateChromosomes() {
        for (int i = 0; i < this.chromosomes.size(); ++i)
            this.chromosomes.get(i).performMutation(this.mutationProbability);
    }

    public void reproduceChromosomes() {
        if (Main.random.nextDouble() < this.crossProbability) {
            Integer pbc = (int) (this.populationSize * this.bestChromosomesRatio);

            if (pbc < 2) {
                pbc = 2;
            }

            ArrayList<ChValue> bestChs = new ArrayList<>(this.fitness.subList(0, pbc));

            ArrayList<Chromosome> children = new ArrayList<>();

            for (ChValue ch: bestChs)
                children.add(ch.ch);

            for (int i = 0; i < this.populationSize - pbc; ++i) {
                Integer split = Main.random.nextInt(this.populationSize);

                Integer parentA = Main.random.nextInt(bestChs.size());
                Integer parentB = Main.random.nextInt(bestChs.size());

                while (parentA == parentB) {
                    parentA = Main.random.nextInt(bestChs.size());
                }

                Chromosome pA = bestChs.get(parentA).ch;
                Chromosome pB = bestChs.get(parentB).ch;

                ArrayList<Integer> joinedGenes = new ArrayList<>(pA.getGenes().subList(0, split));

                ArrayList<Integer> halfParentB = new ArrayList<>(pB.getGenes().subList(split, pB.getSize()));

                for (int g = 0; g < halfParentB.size(); ++g) {
                    Integer gen = halfParentB.get(g);

                    if (!joinedGenes.contains(gen)) {
                        joinedGenes.add(gen);
                    } else {
                        Integer newGen = Main.random.nextInt(this.size);

                        while (halfParentB.contains(newGen) || joinedGenes.contains(newGen)) {
                            newGen = Main.random.nextInt(this.size);
                        }

                        joinedGenes.add(newGen);
                    }
                }

                Chromosome child = new Chromosome(this.size, this.geneMutations, joinedGenes);

                children.add(child);

                this.chromosomes = children;
            }
        }
    }

    public void computeBestChromosome() {
        this.fitness.sort(Comparator.comparingInt((ChValue o) -> o.fitness));
        ChValue best = this.fitness.get(0);

        if (best.fitness < this.bestChromosome.fitness) {
            best.generation = this.iterations;
            this.bestChromosome = best;
        }
    }

    // ########################################################################
    // ######################### GREEDY METHODS ###############################
    // ########################################################################

    public Chromosome greedyTransposition(Chromosome ch) {
        Integer howManyBestOnes = 100;
        ArrayList<ChValue> firstBestOnes = new ArrayList<>();
        ArrayList<Integer> currentGenes = new ArrayList<>(ch.getGenes());

        for (int i = 0; i < this.size; ++i) {
            for (int j = 0; j < this.size; ++j) {
                ArrayList<Integer> copy = new ArrayList<>(currentGenes);

                Integer aux = copy.get(i);
                copy.set(i, copy.get(j));
                copy.set(j, aux);

                Integer transpositionFitness = this.computeFitnessByChromosome(
                        new Chromosome(this.size, this.geneMutations, copy)
                );

                Integer transpositionCurrentGenes = this.computeFitnessByChromosome(
                        new Chromosome(this.size, this.geneMutations, currentGenes)
                );

                if (transpositionFitness < transpositionCurrentGenes) {
                    currentGenes = copy;
                    firstBestOnes.add(new ChValue(
                            new Chromosome(this.size, this.geneMutations, currentGenes),
                            transpositionFitness)
                    );
                }

                if (firstBestOnes.size() == howManyBestOnes)
                    break;
            }

            if (firstBestOnes.size() == howManyBestOnes)
                break;
        }


        if (firstBestOnes.size() == 0)
            return new Chromosome(this.size, this.geneMutations, currentGenes);


        firstBestOnes.sort(Comparator.comparingInt((ChValue o) -> o.fitness));
        return firstBestOnes.get(0).ch;

//        return new Chromosome(this.size, this.geneMutations, currentGenes);
    }

    public void greedyTrain() {
        for (int i = 0; i < this.chromosomes.size(); ++i)
            this.chromosomes.set(i, this.greedyTransposition(this.chromosomes.get(i)));
    }

    // ########################################################################
    // ################################ RUN ###################################
    // ########################################################################

    public void run() {
        long currentTime = System.nanoTime();

        for (int i = 0; i < this.generations; ++i) {
            ++this.iterations;

            if (this.variant == Variant.LAMARCKIAN)
                this.greedyTrain();

            this.computeAllChromosomesFitness();
            this.reproduceChromosomes();
            this.mutateChromosomes();

            if (i == this.generations - 1) {
                this.computeAllChromosomesFitness();
            }

            this.computeBestChromosome();
        }

        this.runTime = (double) (System.nanoTime() - currentTime) / 1000000000;
    }

    @Override
    public String toString() {
        return "Population{" +
                "runTime=" + runTime +
                ", bestChromosome=" + bestChromosome +
                ", iterations=" + iterations +
                ", size=" + size +
                ", populationSize=" + populationSize +
                ", generations=" + generations +
                ", database='" + database + '\'' +
//                ", chromosomes=" + chromosomes +
//                ", flows=" + flows +
//                ", distances=" + distances +
//                ", fitness=" + fitness +
//                ", variant=" + variant +
                ", mutationProbability=" + mutationProbability +
                ", crossProbability=" + crossProbability +
                ", geneMutations=" + geneMutations +
                ", bestChromosomesRatio=" + bestChromosomesRatio +
                ", seed=" + seed +
                '}';
    }
}
