import java.util.*;

public class TACoptimise {

    static Map<String, String> constants = new HashMap<>();
    static Map<String, String> expressions = new HashMap<>();

    static boolean isNumber(String s) {
        return s.matches("-?\\d+");
    }

    static String evaluate(String op1, String op2, String op) {
        int a = Integer.parseInt(op1);
        int b = Integer.parseInt(op2);

        switch (op) {
            case "+": return String.valueOf(a + b);
            case "-": return String.valueOf(a - b);
            case "*": return String.valueOf(a * b);
            case "/": return String.valueOf(a / b);
        }
        return "";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter TAC (type END to stop):");

        List<String> code = new ArrayList<>();

        while (true) {
            String line = sc.nextLine().trim();
            if (line.equalsIgnoreCase("END")) break;
            if (!line.isEmpty()) code.add(line);
        }

        List<String> optimized = new ArrayList<>();

        for (String line : code) {

            String[] parts = line.split("=");
            if (parts.length < 2) continue;

            String lhs = parts[0].trim();
            String rhs = parts[1].trim();

            String[] tokens = rhs.split(" ");

            if (tokens.length == 1) {
                String val = tokens[0];

                if (constants.containsKey(val)) {
                    val = constants.get(val);
                }

                if (isNumber(val)) {
                    constants.put(lhs, val);
                }

                optimized.add(lhs + " = " + val);
            }

            else if (tokens.length == 3) {
                String op1 = tokens[0];
                String op = tokens[1];
                String op2 = tokens[2];

                if (constants.containsKey(op1)) op1 = constants.get(op1);
                if (constants.containsKey(op2)) op2 = constants.get(op2);

                if (isNumber(op1) && isNumber(op2)) {
                    String val = evaluate(op1, op2, op);
                    constants.put(lhs, val);
                    optimized.add(lhs + " = " + val);
                }

                else if (op.equals("+") && op2.equals("0")) {
                    optimized.add(lhs + " = " + op1);
                }
                else if (op.equals("+") && op1.equals("0")) {
                    optimized.add(lhs + " = " + op2);
                }
                else if (op.equals("*") && op2.equals("1")) {
                    optimized.add(lhs + " = " + op1);
                }
                else if (op.equals("*") && op1.equals("1")) {
                    optimized.add(lhs + " = " + op2);
                }

                else {
                    String expr = op1 + " " + op + " " + op2;

                    if (expressions.containsKey(expr)) {
                        optimized.add(lhs + " = " + expressions.get(expr));
                    } else {
                        expressions.put(expr, lhs);
                        optimized.add(lhs + " = " + expr);
                    }
                }
            }
        }

        System.out.println("\nOptimized TAC:\n");
        for (String line : optimized) {
            System.out.println(line);
        }

        sc.close();
    }
}