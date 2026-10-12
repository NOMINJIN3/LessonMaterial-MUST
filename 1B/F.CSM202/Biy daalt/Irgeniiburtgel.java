
import java.util.*;

public class Irgeniiburtgel {
    private List<Irgen> irged = new ArrayList<>();

    public void addIrgen(Irgen i) {
        irged.add(i);
    }

    public List<Irgen> searchByRdugaar(String rdugaar) {
        List<Irgen> result = new ArrayList<>();
        for (Irgen i : irged) {
            String[] parts = i.toString().split(",");
            if (parts.length >= 2 && parts[1].equals(rdugaar)) {
                result.add(i);
            }
        }
        return result;
    }

    public List<Irgen> getAllIrged() {
        return irged;
    }
}

