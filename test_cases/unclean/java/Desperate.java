import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.concurrent.BlockingQueue;

@RestController
public class Desperate {

    // Missing '@Deprecated' annotation on scheduled for removal API
    @Deprecated
    public void deprecatedMethod() {
    }

    @Scheduled(fixedRate = 1000)
    public void scheduledForRemoval() {
        // No @Deprecated annotation - Warning: Missing '@Deprecated' annotation on scheduled for removal API
    }

    // Non-safe string is passed to safe method
    public void unsafeMethod(String input) {
        safeMethod(input); // Warning: Non-safe string is passed to safe method
    }

    private void safeMethod(String input) {
        // Safe method
    }

    // Non-safe string is used as SQL
    public void unsafeSql(String input) {
        String sql = "SELECT * FROM table WHERE column = '" + input + "'"; // Warning: Non-safe string is used as SQL
    }

    // Possibly blocking call in non-blocking context
    public void nonBlockingMethod(BlockingQueue<String> queue) {
        queue.take(); // Warning: Possibly blocking call in non-blocking context
    }

    // Unknown HTTP header
    @RequestMapping("/endpoint")
    public String endpoint() {
        // HttpHeaders headers = new HttpHeaders(); // Uncommenting this line will trigger a warning
        // headers.set("Unknown-Header", "value"); // Uncommenting this line will trigger a warning
        return "Response";
    }

    // Some other issues for variety
    private void unusedPrivateMethod() {
        // Unused private method
    }

    public void unusedMethod() {
        // Unused method
    }

    // Some other deprecated API usage
    public void deprecatedUsage() {
        Connection connection = null;
        PreparedStatement preparedStatement = null;

        try {
            preparedStatement = connection.prepareStatement("SELECT * FROM table");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (preparedStatement != null) {
                    preparedStatement.close(); // Deprecated method
                }
                if (connection != null) {
                    connection.close(); // Deprecated method
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
