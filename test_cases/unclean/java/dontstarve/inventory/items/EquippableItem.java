package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * Felvehető / kézbe vehető item leírására szolgáló osztály.
 */
public abstract class EquippableItem extends AbstractItem {

    /**
     * A trágy használtságát írja le.
     */
    private float durability;

    /**
     * A maximális használhatóság.
     */
    private final float maxDurability;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param type   az item típusa
     */
    public EquippableItem(ItemType type) {
        super(type, 1);
        this.durability = 40;
        this.maxDurability = 40;
    }

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     * @param type típus
     * @param maxDurability maximális használhatóság
     */
    public EquippableItem(ItemType type, float maxDurability) {
        super(type, 1);
        this.durability = maxDurability;
        this.maxDurability = maxDurability;
    }

    /**
     * Megadja, hogy milyen állapotban van a tárgy.
     * @return a tárgy használatlansága, %-ban (100%: tökéletes állapot)
     */
    public float percentage() {
        return this.durability / this.maxDurability * 100;
    }

    /**
     * Csökkenti a durabilityt.
     * @return eltört-e az eszköz
     */
    public boolean decreaseDurability(){
        if(durability == 0){
            return false;
        }
        durability = Math.max(durability-1, 0);
        return durability == 0;
    }
}
