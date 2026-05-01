package LPCC5;
import java.util.*;

public class TACcontrol {

    static int tempCount = 1;
    static int labelCount = 1;

    static String newTemp() {
        return "t" + tempCount++;
    }

    static String newLabel() {
        return "L" + labelCount++;
    }

    static String generateExpr(String expr) {
        Stack<String> operands = new Stack<>();
        Stack<Character> operators = new Stack<>();

        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);

            if (ch == ' ') continue;

            if (Character.isLetterOrDigit(ch)) {
                operands.push(String.valueOf(ch));
            } else {
                while (!operators.isEmpty()) {
                    String op2 = operands.pop();
                    String op1 = operands.pop();
                    char op = operators.pop();

                    String temp = newTemp();
                    System.out.println(temp + " = " + op1 + " " + op + " " + op2);
                    operands.push(temp);
                }
                operators.push(ch);
            }
        }

        while (!operators.isEmpty()) {
            String op2 = operands.pop();
            String op1 = operands.pop();
            char op = operators.pop();

            String temp = newTemp();
            System.out.println(temp + " = " + op1 + " " + op + " " + op2);
            operands.push(temp);
        }

        return operands.pop();
    }

    static void generateIf(String condition, String statement) {
        String[] parts = condition.split("<");
        String left = parts[0].trim();
        String right = parts[1].trim();

        String t1 = newTemp();
        System.out.println(t1 + " = " + left + " < " + right);

        String L1 = newLabel();
        String L2 = newLabel();

        System.out.println("if " + t1 + " goto " + L1);
        System.out.println("goto " + L2);

        System.out.println(L1 + ":");

        String[] stmt = statement.split("=");
        String lhs = stmt[0].trim();
        String rhs = stmt[1].replace(";", "").trim();

        String t2 = generateExpr(rhs);
        System.out.println(lhs + " = " + t2);

        System.out.println(L2 + ":");
    }

    public static void main(String[] args) {

        String condition = "a<b";
        String statement = "a=a-c;";

        System.out.println("Three Address Code:\n");
        generateIf(condition, statement);
    }
}