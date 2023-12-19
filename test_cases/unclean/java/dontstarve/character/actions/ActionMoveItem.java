package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.character.GameCharacter;

/**
 * A tárgy mozgatása akció leírására szolgáló osztály: a tárgyat az inventory-ban egy másik pozícióra mozgatjuk.
 */
public class ActionMoveItem extends Action {
    /**
     * A mozgatni kívánt tárgy pozíciója az inventory-ban.
     */
    private final int oldIndex;

    /**
     * A mozgatni kívánt tárgy új pozíciója az inventory-ban.
     */
    private final int newIndex;

    /**
     * Az akció létrehozására szolgáló konstruktor.
     * @param oldIndex a mozgatni kívánt tárgy pozíciója az inventory-ban
     * @param newIndex a mozgatni kívánt tárgy új pozíciója az inventory-ban
     */
    public ActionMoveItem(int oldIndex, int newIndex) {
        super(ActionType.MOVE_ITEM);
        this.oldIndex = oldIndex;
        this.newIndex = newIndex;
    }

    /**
     * az oldIndex gettere.
     * @return A mozgatni kívánt tárgy pozíciója az inventory-ban
     */
    public int getOldIndex() {
        return oldIndex;
    }

    /**
     * a newIndex gettere.
     * @return A mozgatni kívánt tárgy új pozíciója az inventory-ban
     */
    public int getNewIndex() {
        return newIndex;
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        return character.getInventory().moveItem(getOldIndex(), getNewIndex());
    }
}
