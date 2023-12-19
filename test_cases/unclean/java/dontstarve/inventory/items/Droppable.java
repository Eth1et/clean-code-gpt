package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * Megmondja, hogy az adott item eldobható-e.
 */
public final class Droppable {

    /**
     * Megadja hogy az adott típusú item a földre esik-e, vagy az inventoryba kerül.
     * @param type a típus
     * @return földreesik-e
     */
    public static boolean dropsToGround(ItemType type){
        return type == ItemType.STONE || type == ItemType.LOG;
    }
}
