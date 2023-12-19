package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A nyers bogyó item leírására szolgáló osztály.
 */
public class ItemRawBerry extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 10;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemRawBerry(int amount) {
        super(ItemType.RAW_BERRY, amount);
    }

    /**
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
