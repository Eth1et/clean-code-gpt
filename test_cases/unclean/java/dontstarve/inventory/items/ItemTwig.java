package prog1.kotprog.dontstarve.solution.inventory.items;

/**
 * A gally item leírására szolgáló osztály.
 */
public class ItemTwig extends AbstractItem {

    /**
     * Maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 20;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     *
     * @param amount az item mennyisége
     */
    public ItemTwig(int amount) {
        super(ItemType.TWIG, amount);
    }

    /**
     * @return A maximális stackelhető darabszám
     */
    @Override
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }
}
