package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;

/**
 * Egy általános akadályt leíró absztrakt osztály.
 */
public abstract class InteractiveObject {

    /**
     * Az objektum életereje, ha 0-t eléri akkor kiütöttük.
     */
    private int health;

    /**
     * Az objektum típusa.
     */
    private final InteractiveObjectType type;

    /**
     * Az eszköz amellyel az objektumot ki lehet ütni.
     */
    private final ItemType required;

    /**
     * Interaktív Objektum inicializáló konstruktor.
     * @param type az objektum típusa
     */
    public InteractiveObject(InteractiveObjectType type, ItemType required, int health){
        this.type = type;
        this.required = required;
        this.health = health;
    }

    /**
     * A type gettere.
     * @return a tárgy típusa
     */
    public InteractiveObjectType getType() {
        return type;
    }

    /**
     * @return A szükséges eszköz az objektummal való interaktáláshoz
     */
    public ItemType getRequired(){
        return this.required;
    }

    /**
       A játékos beleüt az adott törhető objektumba és megsebzi.
       @param itemInHand a kézben tartott eszköz típusa
     * @return sikerült-e kiütnie 0, ha nem, az adott nyersanyag mennyisége, ha igen
     */
    public boolean takeHit(ItemType itemInHand){
        if(health == 0 || itemInHand != getRequired()){
            return false;
        }
        health--;
        return health == 0;
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public abstract AbstractItem gatherResource();

    /**
     * Megadja hogy milyen eszközzel lehet kiütni az objektumot.
     * @return A kellő eszköz
     */
    public ItemType requiredToolType(){
        return switch (type){
            case TREE -> ItemType.AXE;
            case STONE -> ItemType.PICKAXE;
            default -> null;
        };
    }

    /**
     * Megadja az életerőt.
     * @return int
     */
    public int getHealth(){
        return health;
    }
}
