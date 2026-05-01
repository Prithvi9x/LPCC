import java.io.*;
import java.util.*;

class AssemblerSecondPass {

    static Map<Integer, Integer> symtab = new HashMap<>();
    static Map<Integer, Integer> littab = new HashMap<>();

    public static void main(String[] args) throws Exception {

        loadSymbolTable();
        loadLiteralTable();

        BufferedReader icReader = new BufferedReader(new FileReader("inter.txt"));
        BufferedWriter output = new BufferedWriter(new FileWriter("output.txt"));

        String line;

        while ((line = icReader.readLine()) != null) {

            line = line.trim();
            if (line.isEmpty()) continue;

            if (line.startsWith("(IS")) {

                String[] parts = line.split(" ");

                // Extract opcode
                String opcodePart = parts[0];
                int opcode = Integer.parseInt(
                        opcodePart.substring(4, opcodePart.length() - 1)
                );

                int reg = 0;
                int memAddr = 0;

                for (String p : parts) {

                    if (p.startsWith("(R")) {
                        reg = Integer.parseInt(
                                p.substring(3, p.length() - 1)
                        );
                    }

                    else if (p.startsWith("(S")) {
                        int index = Integer.parseInt(
                                p.substring(3, p.length() - 1)
                        );
                        memAddr = symtab.get(index);
                    }

                    else if (p.startsWith("(L")) {
                        int index = Integer.parseInt(
                                p.substring(3, p.length() - 1)
                        );
                        memAddr = littab.get(index);
                    }
                }

                output.write(String.format("%02d %02d %03d",
                        opcode, reg, memAddr));
                output.newLine();
            }

            else if (line.startsWith("(DL,01)")) {
                // DC
                int constant = Integer.parseInt(
                        line.substring(line.indexOf("(C,") + 3, line.length() - 1)
                );
                output.write("00 00 " + constant);
                output.newLine();
            }

            else if (line.startsWith("(DL,02)")) {
                continue;
            }
        }

        icReader.close();
        output.close();

        System.out.println("Pass-2 Completed. Machine code in output.txt");
    }

    static void loadSymbolTable() throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("st.txt"));
        String line;
        br.readLine();

        while ((line = br.readLine()) != null) {
            String[] parts = line.split("\\s+");
            int index = Integer.parseInt(parts[0]);
            int address = Integer.parseInt(parts[2]);
            symtab.put(index, address);
        }

        br.close();
    }

    static void loadLiteralTable() throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("lt.txt"));
        String line;
        br.readLine(); // Skip header

        while ((line = br.readLine()) != null) {
            String[] parts = line.split("\\s+");
            int index = Integer.parseInt(parts[0]);
            int address = Integer.parseInt(parts[2]);
            littab.put(index, address);
        }

        br.close();
    }
}
