package prog1.kotprog.dontstarve.solution.character.actions;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.character.GameCharacter;

/**
 * A támadás akció leírására szolgáló osztály: a legközelebbi karakter megtámadása.
 */
public class ActionAttack extends Action {
    /**
     * Az akció létrehozására szolgáló konstruktor.
     */
    public ActionAttack() {
        super(ActionType.ATTACK);
    }

    /**
     * Végrehajtja az akciót az adott karakteren.
     * @param character a karakter
     */
    public boolean execute(GameCharacter character) {
        GameCharacter enemy = GameManager.getInstance().getNearestCharacter(character, 2);
        if(enemy != null){
            character.attack(enemy);
            return true;
        }
        return false;
    }
}
