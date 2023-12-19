package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A nyers répa item leírására szolgáló osztály.
 */
public class ItemRawCarrot extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 10;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemRawCarrot(int amount) {
        super(ItemType.RAW_CARROT, amount);
    }

    /**
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
