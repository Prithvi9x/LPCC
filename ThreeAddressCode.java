package LPCC5;
import java.util.*;

public class ThreeAddressCode {

    static int tempCount = 1;

    static int precedence(char op) {
        if (op == '+' || op == '-') return 1;
        if (op == '*' || op == '/') return 2;
        return 0;
    }

    static String newTemp() {
        return "t" + tempCount++;
    }

    static void process(Stack<String> operands, Stack<Character> operators) {
        String op2 = operands.pop();
        String op1 = operands.pop();
        char op = operators.pop();

        String temp = newTemp();
        System.out.println(temp + " = " + op1 + " " + op + " " + op2);
        operands.push(temp);
    }

    static void generateTAC(String expr) {
        Stack<String> operands = new Stack<>();
        Stack<Character> operators = new Stack<>();

        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);

            if (ch == ' ') continue;

            if (Character.isLetterOrDigit(ch)) {
                operands.push(String.valueOf(ch));
            }
            else if (ch == '(') {
                operators.push(ch);
            }
            else if (ch == ')') {
                while (operators.peek() != '(') {
                    process(operands, operators);
                }
                operators.pop();
            }
            else {
                if (ch == '-' && (i == 0 || expr.charAt(i - 1) == '(' ||
                        "+-*/".indexOf(expr.charAt(i - 1)) != -1)) {

                    char next = expr.charAt(i + 1);

                    String temp = newTemp();
                    System.out.println(temp + " = 0 - " + next);

                    operands.push(temp);
                    i++;
                    continue;
                }

                while (!operators.isEmpty() &&
                        operators.peek() != '(' &&
                        precedence(operators.peek()) >= precedence(ch)) {
                    process(operands, operators);
                }

                operators.push(ch);
            }
        }

        while (!operators.isEmpty()) {
            process(operands, operators);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the expression:");
        String expr = sc.nextLine();

        System.out.println("\nThree Address Code:");
        generateTAC(expr);

        sc.close();
    }
}