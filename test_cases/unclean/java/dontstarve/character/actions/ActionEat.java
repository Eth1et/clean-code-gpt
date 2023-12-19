package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.character.GameCharacter;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;

/**
 * Az étel elfogyasztása akció leírására szolgáló osztály: egy étel elfogyasztása az inventory-ból.
 */
public class ActionEat extends Action {
    /**
     * A megenni kívánt étel pozíciója az inventory-ban.
     */
    private final int index;

    /**
     * Az akció létrehozására szolgáló konstruktor.
     *
     * @param index a megenni kívánt étel pozíciója az inventory-ban
     */
    public ActionEat(int index) {
        super(ActionType.EAT);
        this.index = index;
    }

    /**
     * Az index gettere.
     * @return a megenni kívánt étel pozíciója az inventory-ban
     */
    public int getIndex() {
        return index;
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        ItemType type = character.getInventory().eatItem(index);
        if(type == null){
            return false;
        }
        switch (type){
            case RAW_BERRY -> character.heal(-5, 20);
            case RAW_CARROT -> character.heal(1, 12);
            case COOKED_BERRY -> character.heal(1, 10);
            case COOKED_CARROT -> character.heal(3, 10);
        }
        return true;
    }
}
