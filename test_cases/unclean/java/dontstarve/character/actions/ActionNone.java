package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.character.GameCharacter;

/**
 * A várakozás akció leírására szolgáló osztály: a karakter nem végez cselekvést az aktuális körben.
 */
public class ActionNone extends Action {
    /**
     * Az akció létrehozására szolgáló konstruktor.
     */
    public ActionNone() {
        super(ActionType.NONE);
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        return true;
    }
}
