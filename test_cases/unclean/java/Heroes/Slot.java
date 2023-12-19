package Heroes;

import javafx.scene.control.Label;
import javafx.scene.image.ImageView;

/**
 * Az osztály a játékban lévő inventory sáv egy-egy egységét valósítja meg.
 */
public class Slot {
    private Label title, counter;
    private ImageView icon;

    public Slot(Label title, Label counter, ImageView icon) {
        this.title = title;
        this.counter = counter;
        this.icon = icon;
    }

    public Label getTitle() {
        return title;
    }

    public Label getCounter() {
        return counter;
    }

    public ImageView getIcon() {
        return icon;
    }
}
