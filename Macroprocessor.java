import java.io.*;
import java.util.*;

public class Macroprocessor {

    static class MNTEntry {
        String name;
        int paramCount;
        int mdtIndex;

        MNTEntry(String name, int paramCount, int mdtIndex) {
            this.name = name;
            this.paramCount = paramCount;
            this.mdtIndex = mdtIndex;
        }
    }

    static List<String> MDT = new ArrayList<>();
    static List<MNTEntry> MNT = new ArrayList<>();

    public static void main(String[] args) {
        try {
            pass1();
            pass2();
            System.out.println("Macro Processing Completed Successfully.");
        } catch (Exception e) {
            System.out.println("ERROR: " + e.getMessage());
        }
    }

    // PASS 1 
    static void pass1() throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        BufferedWriter mdtWriter = new BufferedWriter(new FileWriter("mdt.txt"));
        BufferedWriter mntWriter = new BufferedWriter(new FileWriter("mnt.txt"));

        String line;
        int mdtIndex = 0;

        while ((line = br.readLine()) != null) {

            line = line.trim();

            if (line.startsWith("MACRO")) {

                String header = line.substring(5).trim();
                if (header.isEmpty())
                    throw new Exception("Macro name missing after MACRO");

                String[] parts = header.split("[ ,]+");
                String macroName = parts[0];
                int paramCount = parts.length - 1;

                // Duplicate macro check
                for (MNTEntry e : MNT)
                    if (e.name.equals(macroName))
                        throw new Exception("Duplicate macro definition: " + macroName);

                MNT.add(new MNTEntry(macroName, paramCount, mdtIndex));

                // Formal parameter ALA
                Map<String, String> ala = new HashMap<>();
                for (int i = 1; i < parts.length; i++)
                    ala.put(parts[i], "#" + i);

                boolean mendFound = false;

                while ((line = br.readLine()) != null) {

                    line = line.trim();

                    if (line.equals("MEND")) {
                        mendFound = true;
                        break;
                    }

                    for (String p : ala.keySet())
                        line = line.replace(p, ala.get(p));

                    String[] words = line.split("[ ,]+");

                    //Nested macro expansion
                    MNTEntry nested = null;
                    for (MNTEntry e : MNT)
                        if (e.name.equals(words[0]))
                            nested = e;

                    if (nested != null) {

                        if (words.length - 1 != nested.paramCount)
                            throw new Exception("Incorrect nested macro arguments for " + nested.name);

                        Map<String, String> nestedALA = new HashMap<>();
                        for (int i = 1; i <= nested.paramCount; i++)
                            nestedALA.put("#" + i, words[i]);

                        int idx = nested.mdtIndex;

                        while (!MDT.get(idx).equals("MEND")) {

                            String nestedLine = MDT.get(idx);

                            for (String k : nestedALA.keySet())
                                nestedLine = nestedLine.replace(k, nestedALA.get(k));

                            MDT.add(nestedLine);
                            mdtWriter.write(nestedLine);
                            mdtWriter.newLine();
                            mdtIndex++;
                            idx++;
                        }

                    } else {
                        MDT.add(line);
                        mdtWriter.write(line);
                        mdtWriter.newLine();
                        mdtIndex++;
                    }
                }

                if (!mendFound)
                    throw new Exception("MEND missing for macro: " + macroName);

                MDT.add("MEND");
                mdtWriter.write("MEND");
                mdtWriter.newLine();
                mdtIndex++;
            }
        }

        // Write MNT
        for (MNTEntry e : MNT) {
            mntWriter.write(e.name + " " + e.paramCount + " " + e.mdtIndex);
            mntWriter.newLine();
        }

        br.close();
        mdtWriter.close();
        mntWriter.close();
    }

    //PASS 2 
    static void pass2() throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        BufferedWriter output = new BufferedWriter(new FileWriter("output.txt"));
        BufferedWriter alaWriter = new BufferedWriter(new FileWriter("ala.txt"));

        String line;

        while ((line = br.readLine()) != null) {

            line = line.trim();

            if (line.startsWith("MACRO")) {
                while (!(line = br.readLine()).trim().equals("MEND"));
                continue;
            }

            if (line.isEmpty()) {
                output.newLine();
                continue;
            }

            String[] parts = line.split("[ ,]+");
            String word = parts[0];

            MNTEntry found = null;
            for (MNTEntry e : MNT)
                if (e.name.equals(word))
                    found = e;

            if (found != null) {

                if (parts.length - 1 != found.paramCount)
                    throw new Exception("Incorrect number of arguments in call to " + found.name);

                Map<String, String> ala = new HashMap<>();
                for (int i = 1; i <= found.paramCount; i++) {
                    ala.put("#" + i, parts[i]);
                    alaWriter.write(i + " " + parts[i]);
                    alaWriter.newLine();
                }

                int idx = found.mdtIndex;

                while (!MDT.get(idx).equals("MEND")) {

                    String expanded = MDT.get(idx);

                    for (String k : ala.keySet())
                        expanded = expanded.replace(k, ala.get(k));

                    output.write(expanded);
                    output.newLine();
                    idx++;
                }

            } else {
                output.write(line);
                output.newLine();
            }
        }

        br.close();
        output.close();
        alaWriter.close();
    }
}