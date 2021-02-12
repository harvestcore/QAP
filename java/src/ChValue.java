public class ChValue {
    public Chromosome ch = null;
    public Integer fitness = Integer.MAX_VALUE;
    public Integer generation = 0;

    public ChValue() {}

    public ChValue(Chromosome ch, Integer fitness) {
        this.ch = ch;
        this.fitness = fitness;
    }

    @Override
    public String toString() {
        return "ChValue{" +
                "fitness=" + fitness +
                ", ch=" + ch +
                ", generation=" + generation +
                '}';
    }
}
