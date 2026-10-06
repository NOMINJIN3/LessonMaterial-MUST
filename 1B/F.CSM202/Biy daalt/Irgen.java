
public class Irgen {

    static class Hayag {
        String aimagHot;
        String sumDuureg;
        String gudamjBag;

        public Hayag(String aimagHot, String sumDuureg, String gudamjBag) {
            this.aimagHot = aimagHot;
            this.sumDuureg = sumDuureg;
            this.gudamjBag = gudamjBag;
        }

        @Override
        public String toString() {
            return aimagHot + ", " + sumDuureg + ", " + gudamjBag;
        }
    }

    String ner;
    String rdugaar;
    String tursunudur;
    String huis;
    Hayag hayag;

    public Irgen(String ner, String rdugaar, String tursunudur, String huis, Hayag hayag) {
        this.ner = ner;
        this.rdugaar = rdugaar;
        this.tursunudur = tursunudur;
        this.huis = huis;
        this.hayag = hayag;
    }

    @Override
    public String toString() {
        return "Ner: " + ner + "\nRDugaar: " + rdugaar + "\nTursunudur: " + tursunudur +
                "\nHuis: " + huis + "\nHayag: " + hayag;
    }


    public static void main(String[] args) {
        Hayag h = new Hayag("Ulaanbaatar", "Suhbaatar", "1-r horoo");
        Irgen irgen = new Irgen("Bold", "AB12345678", "1990-01-01", "Er", h);

        System.out.println(irgen);

    }
}
   

    

     