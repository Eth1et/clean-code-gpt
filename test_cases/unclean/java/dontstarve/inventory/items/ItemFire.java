package prog1.kotprog.dontstarve.solution.inventory.items;

import java.util.HashMap;
import java.util.Map;

/**
 * A fire item leírására szolgáló osztály.
 */
public class ItemFire extends AbstractItem {

    /**
     * A kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    private final Map<ItemType, Integer> requiredResource = new HashMap<>() {
        {
            put(ItemType.TWIG, 2);
            put(ItemType.LOG, 2);
            put(ItemType.STONE, 4);
        }
    };

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     */
    public ItemFire() {
        super(ItemType.FIRE, 1);
    }

    /**
     * @return Visszaadja a kraftoláshoz szükséges tárgyak, mennyiségük
     */
    public Map<ItemType, Integer> getRequiredResource() {
        return requiredResource;
    }
}
