package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A fa item leírására szolgáló osztály.
 */
public class ItemLog extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 15;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemLog(int amount) {
        super(ItemType.LOG, amount);
    }

    /**
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
