package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A kő item leírására szolgáló osztály.
 */
public class ItemStone extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 10;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemStone(int amount) {
        super(ItemType.STONE, amount);
    }

    /**
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
