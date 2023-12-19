package prog1.kotprog.dontstarve.solution.level;

import prog1.kotprog.dontstarve.solution.level.interactive.TreeObject;
import prog1.kotprog.dontstarve.solution.level.interactive.TwigObject;
import prog1.kotprog.dontstarve.solution.level.interactive.StoneObject;
import prog1.kotprog.dontstarve.solution.level.interactive.BerryObject;
import prog1.kotprog.dontstarve.solution.level.interactive.CarrotObject;

/**
 * A betöltendő mapen előforduló színek enumja.
 */
public class MapColors {
    /**
     * Üres mező.
     */
    static final int EMPTY = 0xFF32C832;

    /**
     * Vizet tartalmazó mező.
     */
    static final int WATER = 0xFF3264C8;

    /**
     * Fát tartalmazó mező.
     */
    static final int TREE = 0xFFC86432;

    /**
     * Követ tartalmazó mező.
     */
    static final int STONE = 0xFFC8C8C8;

    /**
     * Gallyat tartalmazó mező.
     */
    static final int TWIG = 0xFFF0B478;

    /**
     * Bogyót tartalmazó mező.
     */
    static final int BERRY = 0xFFFF0000;

    /**
     * Répát tartalmazó mező.
     */
    static final int CARROT = 0xFFFAC800;

    /**
     * Megad az adott színhez egy új mezőt.
     * @param color a szín
     * @return a létrehozott új mező objektum
     */
    public static Field getFieldByColor(int color){
        return switch (color) {
            case EMPTY -> new Field(true, null);
            case WATER -> new Field(false, null);
            case TREE -> new Field(true, new TreeObject());
            case STONE -> new Field(true, new StoneObject());
            case TWIG -> new Field(true, new TwigObject());
            case BERRY -> new Field(true, new BerryObject());
            default -> new Field(true, new CarrotObject());
        };
    }
}
