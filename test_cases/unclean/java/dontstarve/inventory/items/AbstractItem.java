package prog1.kotprog.dontstarve.solution.inventory.items;

import java.util.HashMap;
import java.util.Map;

/**
 * Egy általános itemet leíró osztály.
 */
public abstract class AbstractItem {

    /**
     * A maximum stackelhető mennyiség.
     */
    private static final int MAX_AMOUNT = 1;

    /**
     * Az item mennyisége.
     */
    protected int amount;

    /**
     * A kraftoláshoz szükséges tárgyak, mennyiségük, (ebben az esetben semmi).
     */
    private final Map<ItemType, Integer> requiredResource = new HashMap<>();

    /**
     * Az item típusa.
     * @see ItemType
     */
    private final ItemType type;

    /**
     * Konstruktor, amellyel a tárgy létrehozható.
     * @param type az item típusa
     * @param amount az item mennyisége
     */
    public AbstractItem(ItemType type, int amount) {
        this.type = type;
        this.amount = amount;
    }

    /**
     * @return Visszaadja a kraftoláshoz szükséges tárgyak, mennyiségük.
     */
    public Map<ItemType, Integer> getRequiredResource() {
        return requiredResource;
    }

    /**
     * A type gettere.
     * @return a tárgy típusa
     */
    public ItemType getType() {
        return type;
    }

    /**
     * Az amount gettere.
     * @return a tárgy mennyisége
     */
    public int getAmount() {
        return amount;
    }


    /**
     * @return A maximális stackelhető darabszám.
     */
    public int getMaxAmount() {
        return MAX_AMOUNT;
    }

    /**
     * Az amount settere.
     * @param amount a beállítandó érték
     */
    public void setAmount(int amount){
        this.amount = Math.max(0, amount);
    }
}
