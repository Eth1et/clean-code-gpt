package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.character.GameCharacter;
import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;
import prog1.kotprog.dontstarve.solution.level.Field;

/**
 * A kraftolás akció leírására szolgáló osztály: adott típusú item kraftolása.
 */
public class ActionCraft extends Action {
    /**
     * A lekraftolandó item típusa.
     */
    private final ItemType itemType;

    /**
     * Az akció létrehozására szolgáló konstruktor.
     *
     * @param itemType a lekraftolandó item típusa
     */
    public ActionCraft(ItemType itemType) {
        super(ActionType.CRAFT);
        this.itemType = itemType;
    }

    /**
     * Az itemType gettere.
     *
     * @return a lekraftolandó item típusa
     */
    public ItemType getItemType() {
        return itemType;
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     *
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        Field fieldOfCharacter = GameManager.getInstance().getFieldByPosition(character.getCurrentPosition());
        if (fieldOfCharacter == null) {
            return false;
        }
        if (getItemType() == ItemType.FIRE && fieldOfCharacter.getInteractiveObject() != null) {
            return false;
        }

        AbstractItem item = character.getInventory().craftItem(getItemType());

        if (item != null) {
            if (item.getType() == ItemType.FIRE){
                fieldOfCharacter.placeFire();
            } else {
                fieldOfCharacter.addItem(item);
            }
        }
        return true;
    }
}
