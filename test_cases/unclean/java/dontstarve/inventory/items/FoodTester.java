package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * Class ami megmondja egy adott típusról hogy étel-e.
 */
public final class FoodTester {

    /**
     * Megadja hogy az adott objektum étel-e.
     * @return boolean
     */
    public static boolean isFood(ItemType type){
        return type == ItemType.RAW_BERRY || type == ItemType.RAW_CARROT || type == ItemType.COOKED_BERRY || type == ItemType.COOKED_CARROT;
    }
}
