package prog1.kotprog.dontstarve.solution.inventory.items;

import java.util.HashMap;
import java.util.Map;

/**
 * A csákány item leírására szolgáló osztály.
 */
public class ItemPickaxe extends EquippableItem {

    /**
     * A kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    private final Map<ItemType, Integer> requiredResource = new HashMap<>() {
        {
            put(ItemType.LOG, 2);
            put(ItemType.TWIG, 2);
        }
    };

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     */
    public ItemPickaxe() {
        super(ItemType.PICKAXE, 30);
    }


    /**
     * @return Visszaadja a kraftoláshoz szükséges tárgyak, mennyiségük
     */
    public Map<ItemType, Integer> getRequiredResource() {
        return requiredResource;
    }
}
