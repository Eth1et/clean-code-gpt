package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A főtt répa item leírására szolgáló osztály.
 */
public class ItemCookedCarrot extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 10;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemCookedCarrot(int amount) {
        super(ItemType.COOKED_CARROT, amount);
    }

    /**
     * A maximális stackelhető mennyiség gettere.
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
