package prog1.kotprog.dontstarve.solution.inventory.items;

import java.util.HashMap;
import java.util.Map;

/**
 * A fejsze item leírására szolgáló osztály.
 */
public class ItemAxe extends EquippableItem {

    /**
     * A kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    private final Map<ItemType, Integer> requiredResource = new HashMap<>() {
        {
            put(ItemType.TWIG, 3);
        }
    };

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     */
    public ItemAxe() {
        super(ItemType.AXE, 40);
    }

    /**
     * @return Visszaadja a kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    public Map<ItemType, Integer> getRequiredResource() {
        return requiredResource;
    }
}
