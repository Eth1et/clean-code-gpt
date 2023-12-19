package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.character.GameCharacter;

/**
 * A tárgy kézbe vétele akció leírására szolgáló osztály: egy inventory-ban lévő felvehető tárgy kézbe vétele.
 */
public class ActionEquip extends Action {
    /**
     * A felvenni kívánt tárgy pozíciója az inventory-ban.
     */
    private final int index;

    /**
     * Az akció létrehozására szolgáló konstruktor.
     *
     * @param index a felvenni kívánt tárgy pozíciója az inventory-ban
     */
    public ActionEquip(int index) {
        super(ActionType.EQUIP);
        this.index = index;
    }

    /**
     * Az index gettere.
     * @return a felvenni kívánt tárgy pozíciója az inventory-ban
     */
    public int getIndex() {
        return index;
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        return character.getInventory().equipItem(index);
    }
}
