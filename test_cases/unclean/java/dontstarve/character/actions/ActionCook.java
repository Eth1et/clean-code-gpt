package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.character.GameCharacter;
import prog1.kotprog.dontstarve.solution.inventory.Inventory;
import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemCookedBerry;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemCookedCarrot;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;
import prog1.kotprog.dontstarve.solution.level.Field;

/**
 * A főzés akció leírására szolgáló osztály: egy item megfőzése.
 */
public class ActionCook extends Action {
    /**
     * A megfőzni kívánt tárgy pozíciója az inventory-ban.
     */
    private final int index;

    /**
     * Az akció létrehozására szolgáló konstruktor.
     *
     * @param index a megfőzni kívánt tárgy pozíciója az inventory-ban
     */
    public ActionCook(int index) {
        super(ActionType.COOK);
        this.index = index;
    }

    /**
     * Az index gettere.
     *
     * @return a megfőzni kívánt tárgy pozíciója az inventory-ban
     */
    public int getIndex() {
        return index;
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     *
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        Field field = GameManager.getInstance().getFieldByPosition(character.getCurrentPosition());
        if (field == null || !field.hasFire()) {
            return false;
        }

        Inventory inventory = (Inventory) character.getInventory();
        ItemType itemType = inventory.cookItem(index);
        AbstractItem addedItem = null;

        if (itemType == ItemType.RAW_BERRY) {
            addedItem = new ItemCookedBerry(1);
        } else if (itemType == ItemType.RAW_CARROT) {
            addedItem = new ItemCookedCarrot(1);
        }

        if (addedItem != null && !inventory.addItem(addedItem)) {
            field.addItem(addedItem);
        }
        return true;
    }
}
