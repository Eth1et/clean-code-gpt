package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * Az osztály amely segítségével létrehozhatunk új AbstractItem-eket a megadott típus alapján.
 */
public final class ItemCreator {

    /**
     * Létrehoz egy új példányt az adott típusú gyerekből.
     * @param type a típus
     * @return a létrehozott gyerek
     */
    public static AbstractItem newItemByType(ItemType type){
        return switch (type){
            case FIRE -> new ItemFire();
            case STONE -> new ItemStone(1);
            case LOG -> new ItemLog(1);
            case TWIG -> new ItemTwig(1);
            case RAW_BERRY -> new ItemRawBerry(1);
            case RAW_CARROT -> new ItemRawCarrot(1);
            case COOKED_BERRY -> new ItemCookedBerry(1);
            case COOKED_CARROT -> new ItemCookedCarrot(1);
            default -> ItemCreator.newToolByType(type);
        };
    }

    /**
     * Létrehoz az adott típusú eszközből egy újat.
     * @param type a típus
     * @return a létrehozott eszköz
     */
    public static EquippableItem newToolByType(ItemType type){
        if(type == null){
            return null;
        }

        return switch (type){
            case AXE -> new ItemAxe();
            case PICKAXE -> new ItemPickaxe();
            case SPEAR -> new ItemSpear();
            case TORCH -> new ItemTorch();
            default -> null;
        };
    }
}
