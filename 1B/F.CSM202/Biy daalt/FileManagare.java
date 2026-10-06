import java.io.*;
import java.util.*;

public class FileManager {
    public static List<Citizen> readCitizens(String filename) throws IOException {
        List<Citizen> citizens = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",");
            if (parts.length >= 7) {
                Address addr = new Address(parts[4], parts[5], parts[6]);
                Citizen c = new Citizen(parts[0], parts[1], parts[2], parts[3], addr);
                citizens.add(c);
            }
        }
        reader.close();
        return citizens;
    }

    public static void writeCitizens(String filename, List<Citizen> citizens) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
        for (Citizen c : citizens) {
            writer.write(c.toString());
            writer.newLine();
        }
        writer.close();
    }
}
