
public class Hayag {
    private String aimag;
    private String duureg;
    private String gudamj;

    public Hayag(String aimag, String duureg, String gudamj) {
        this.aimag = aimag;
        this.duureg = duureg;
        this.gudamj = gudamj;
    }

    @Override
    public String toString() {
        return aimag + "," + duureg + "," + gudamj;
    }

    public static void main(String[] args) {
        Hayag h = new Hayag("Ulaanbaatar", "Bayanzurkh", "13-r horoolol");
        System.out.println(h);

    }

}
