package prog1.kotprog.dontstarve.solution.inventory.items;

import java.util.HashMap;
import java.util.Map;

/**
 * A fáklya item leírására szolgáló osztály.
 */
public class ItemTorch extends EquippableItem {

    /**
     * A kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    private final Map<ItemType, Integer> requiredResource = new HashMap<>() {
        {
            put(ItemType.LOG, 1);
            put(ItemType.TWIG, 3);
        }
    };

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     */
    public ItemTorch() {
        super(ItemType.TORCH, 20);
    }


    /**
     * @return Visszaadja a kraftoláshoz szükséges tárgyak, mennyiségük
     */
    public Map<ItemType, Integer> getRequiredResource() {
        return requiredResource;
    }
}
