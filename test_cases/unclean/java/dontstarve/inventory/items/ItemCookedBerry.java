package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A főtt bogyó item leírására szolgáló osztály.
 */
public class ItemCookedBerry extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 10;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemCookedBerry(int amount) {
        super(ItemType.COOKED_BERRY, amount);
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
