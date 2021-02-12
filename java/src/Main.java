import java.util.Random;
import java.util.UUID;

public class Main {
    public static Random random;

    public static void main(String[] args) {
        UUID seed = UUID.randomUUID();
        random = new Random(seed.getLeastSignificantBits() & Long.MAX_VALUE);

        Population p = new Population(
                "databases/tai256c.dat",
                200,
                5000,
                Variant.STANDARD,
                0.7,
                0.7,
                1,
                0.3,
                seed
        );
        p.run();
        System.out.println("\n" + p);
//
//
//        Population p2 = new Population(
//                "databases/tai256c.dat",
//                30,
//                30,
//                Variant.BALDWINIAN,
//                0.6,
//                0.6,
//                1,
//                0.3,
//                seed
//        );
//        p2.run();
//        System.out.println("\n" + p2);

//        Population p3 = new Population(
//                "databases/tai256c.dat",
//                10,
//                5,
//                Variant.LAMARCKIAN,
//                0.5,
//                0.5,
//                1,
//                0.2,
//                seed
//        );
//        p3.run();
//        System.out.println("\n" + p3);
    }
}
