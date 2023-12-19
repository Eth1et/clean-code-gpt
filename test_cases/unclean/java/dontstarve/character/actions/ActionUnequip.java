package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.character.GameCharacter;
import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.level.Field;

/**
 * A tárgy levétele akció leírására szolgáló osztály: az aktuálisan kézben lévő item visszarakása az inventory-ba.
 */
public class ActionUnequip extends Action {
    /**
     * Az akció létrehozására szolgáló konstruktor.
     */
    public ActionUnequip() {
        super(ActionType.UNEQUIP);
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        if(character.getInventory().equippedItem() == null){
            return false;
        }

        Field f = GameManager.getInstance().getFieldByPosition(character.getCurrentPosition().getNearestWholePosition());
        AbstractItem item = character.getInventory().unequipItem();

        if(f != null && item != null){
            f.addItem(item);
        }
        return true;
    }
}
