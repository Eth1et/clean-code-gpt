package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A tárgy típusok enumja.
 */
public enum ItemType {
    /**
     * fejsze.
     */
    AXE,

    /**
     * csákány.
     */
    PICKAXE,

    /**
     * lándzsa.
     */
    SPEAR,

    /**
     * fáklya.
     */
    TORCH,

    /**
     * farönk.
     */
    LOG,

    /**
     * kő.
     */
    STONE,

    /**
     * gally.
     */
    TWIG,


    /**
     * nyers bogyó.
     */
    RAW_BERRY,

    /**
     * nyers répa.
     */
    RAW_CARROT,

    /**
     * főtt bogyó.
     */
    COOKED_BERRY,

    /**
     * főtt répa.
     */
    COOKED_CARROT,

    /**
     * tábortűz (inventory-ban nem tárolható!).
     */
    FIRE;

    /**
     * Megadja hogy az adott típusú tárgy kraftolható-e.
     * @param type a típus
     * @return boolean
     */
    public static boolean craftable(ItemType type){
        return type == ItemType.AXE || type == ItemType.FIRE || type == ItemType.PICKAXE || type == ItemType.SPEAR || type == ItemType.TORCH;
    }
}
