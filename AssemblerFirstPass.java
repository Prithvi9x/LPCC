import java.io.*;
import java.util.*;

class AssemblerFirstPass {

    static class Literal {
        String value;
        int address;
        boolean assigned;

        Literal(String value) {
            this.value = value;
            this.assigned = false;
        }
    }

    static Map<String, Integer> symtab = new LinkedHashMap<>();
    static List<Literal> littab = new ArrayList<>();
    static List<Integer> pooltab = new ArrayList<>();
    static List<String> intermediate = new ArrayList<>();

    static Set<String> usedSymbols = new HashSet<>();
    static boolean errorFound = false;

    static int LC = 0;

    static Map<String, Integer> opcodeIS = new HashMap<>();
    static {
        opcodeIS.put("ADD", 1);
        opcodeIS.put("SUB", 2);
        opcodeIS.put("MULT", 3);
        opcodeIS.put("MOVER", 4);
        opcodeIS.put("MOVEM", 5);
        opcodeIS.put("COMP", 6);
        opcodeIS.put("BC", 7);
        opcodeIS.put("DIV", 8);
        opcodeIS.put("READ", 9);
        opcodeIS.put("PRINT", 10);
        opcodeIS.put("STOP", 0);
    }

    static Map<String, Integer> opcodeDL = new HashMap<>();
    static {
        opcodeDL.put("DC", 1);
        opcodeDL.put("DS", 2);
    }

    static Map<String, Integer> opcodeAD = new HashMap<>();
    static {
        opcodeAD.put("START", 1);
        opcodeAD.put("END", 2);
        opcodeAD.put("LTORG", 5);
    }

    static Map<String, Integer> registerCode = new HashMap<>();
    static {
        registerCode.put("AREG", 1);
        registerCode.put("BREG", 2);
        registerCode.put("CREG", 3);
        registerCode.put("DREG", 4);
    }

    public static void main(String[] args) throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("error_input.txt"));

        pooltab.add(0);

        String line;

        while ((line = br.readLine()) != null) {

            line = line.trim();
            if (line.isEmpty()) continue;

            String[] tokens = line.replace(",", "").split("\\s+");

            if (tokens[0].equals("START")) {
                LC = Integer.parseInt(tokens[1]);
                intermediate.add("(AD,01) (C," + LC + ")");
                continue;
            }

            if (tokens[0].equals("END")) {
                assignLiterals();
                intermediate.add("(AD,02)");
                break;
            }

            if (tokens[0].equals("LTORG")) {
                assignLiterals();
                intermediate.add("(AD,05)");
                continue;
            }

            int index = 0;

            // Label Handling with Duplicate Check
            if (!opcodeIS.containsKey(tokens[0]) &&
                !opcodeDL.containsKey(tokens[0]) &&
                !opcodeAD.containsKey(tokens[0])) {

                if (symtab.containsKey(tokens[0]) && symtab.get(tokens[0]) != -1) {
                    System.out.println("Error: Duplicate definition of symbol -> " + tokens[0]);
                    errorFound = true;
                } else {
                    symtab.put(tokens[0], LC);
                }
                index = 1;
            }

            String op = tokens[index];

            // Invalid Mnemonic Check
            if (!opcodeIS.containsKey(op) &&
                !opcodeDL.containsKey(op) &&
                !opcodeAD.containsKey(op)) {

                System.out.println("Error: Invalid mnemonic -> " + op);
                errorFound = true;
                continue;
            }

            // Imperative Statement
            if (opcodeIS.containsKey(op)) {

                StringBuilder ic = new StringBuilder();
                ic.append("(IS," + String.format("%02d", opcodeIS.get(op)) + ") ");

                if (!op.equals("STOP")) {

                    if (registerCode.containsKey(tokens[index + 1])) {
                        ic.append("(R," + registerCode.get(tokens[index + 1]) + ") ");
                    }

                    if (tokens.length > index + 2) {

                        String operand = tokens[index + 2];

                        if (operand.startsWith("='")) {
                            int litIndex = getLiteralIndex(operand);
                            ic.append("(L," + (litIndex + 1) + ")");
                        } else {
                            symtab.putIfAbsent(operand, -1);
                            usedSymbols.add(operand);
                            int symIndex = new ArrayList<>(symtab.keySet()).indexOf(operand);
                            ic.append("(S," + (symIndex + 1) + ")");
                        }
                    }
                }

                intermediate.add(ic.toString());
                LC++;
            }

            // Declarative Statement
            else if (opcodeDL.containsKey(op)) {

                intermediate.add("(DL," +
                        String.format("%02d", opcodeDL.get(op)) +
                        ") (C," + tokens[index + 1] + ")");

                if (op.equals("DS")) {
                    LC += Integer.parseInt(tokens[index + 1]);
                } else {
                    LC++;
                }
            }
        }

        br.close();

        // Check for undeclared symbols
        for (Map.Entry<String, Integer> entry : symtab.entrySet()) {
            if (entry.getValue() == -1) {
                System.out.println("Error: Symbol not declared -> " + entry.getKey());
                errorFound = true;
            }
        }

        // Warning: declared but not used
        for (String symbol : symtab.keySet()) {
            if (!usedSymbols.contains(symbol)) {
                System.out.println("Warning: Symbol declared but not used -> " + symbol);
            }
        }

        if (errorFound) {
            System.out.println("Assembly failed due to errors.");
            return;
        }

        writeTables();
        System.out.println("All files generated successfully.");
    }

    static int getLiteralIndex(String literal) {
        for (int i = 0; i < littab.size(); i++) {
            if (littab.get(i).value.equals(literal))
                return i;
        }
        littab.add(new Literal(literal));
        return littab.size() - 1;
    }

    static void assignLiterals() {
        for (Literal lit : littab) {
            if (!lit.assigned) {
                lit.address = LC;
                lit.assigned = true;
                LC++;
            }
        }
    }

    static void writeTables() throws Exception {

        BufferedWriter st = new BufferedWriter(new FileWriter("st.txt"));
        st.write("Index\tSymbol\tAddress\n");
        int i = 1;
        for (Map.Entry<String, Integer> entry : symtab.entrySet()) {
            st.write(i++ + "\t" + entry.getKey() + "\t" + entry.getValue() + "\n");
        }
        st.close();

        BufferedWriter lt = new BufferedWriter(new FileWriter("lt.txt"));
        lt.write("Index\tLiteral\tAddress\n");
        for (int j = 0; j < littab.size(); j++) {
            lt.write((j + 1) + "\t" +
                    littab.get(j).value + "\t" +
                    littab.get(j).address + "\n");
        }
        lt.close();

        BufferedWriter pt = new BufferedWriter(new FileWriter("pl.txt"));
        pt.write("PoolNo\tStartIndex\n");
        for (int k = 0; k < pooltab.size(); k++) {
            pt.write((k + 1) + "\t" + (pooltab.get(k) + 1) + "\n");
        }
        pt.close();

        BufferedWriter ic = new BufferedWriter(new FileWriter("inter.txt"));
        for (String s : intermediate) {
            ic.write(s + "\n");
        }
        ic.close();
    }
}
