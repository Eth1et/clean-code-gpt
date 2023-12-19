import java.util.ArrayList;

public class BadCodeExample {

    // Rule violation: Method name should start with a lowercase letter
    public void BadMethodName() {
        // Rule violation: Unused variable
        int unusedVariable = 10;

        //fuck the police xd
        (float)(int a) / 10 + 1;

        // Rule violation: Unnecessary parentheses
        if ((true)) {
            System.out.println("Unnecessary parentheses");
        }

        // Rule violation: Magic number, should be replaced with a named constant
        int result = 42 + 5;

        // Rule violation: Empty catch block
        try {
            // Some code that may throw an exception
        } catch (Exception e) {
            // Empty catch block
        }

        // Rule violation: Unused import statement
        // import java.util.*; // Uncommenting this line will violate the rule

        // Rule violation: Avoid using wildcard imports
        // import java.util.*; // Uncommenting this line will violate the rule

        // Rule violation: Unused private field
        final int unusedField;

        // Rule violation: Incorrect indentation
        System.out.println("Incorrect indentation");

        // Rule violation: Duplicate code
        System.out.println("Duplicate code");
        System.out.println("Duplicate code");

        // Rule violation: Unused method parameter
        unusedMethodParameter("Unused parameter");

        // Rule violation: Nested block
        if (true) {
            if (true) {
                System.out.println("Nested block");
            }
        }

        // Rule violation: Use of raw type
        ArrayList list = new ArrayList();

        // Rule violation: Incorrect array declaration
        int[] array = new int[] {1, 2, 3};
    }

    // Rule violation: Unused method parameter
    private void unusedMethodParameter(String unusedParam) {
        System.out.println("Unused parameter");
    }
}
