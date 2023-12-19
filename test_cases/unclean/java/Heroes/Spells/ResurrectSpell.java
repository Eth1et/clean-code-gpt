package Heroes.Spells;

import Heroes.Enums.SpellType;
import Heroes.GameManager;
import Heroes.Units.BattleUnit;

/**
 * A képesség specializálása, a Feltámasztás működését valósítja meg.
 */
public class ResurrectSpell extends Spell{
    private static final int HEALFORCE = 50;

    public ResurrectSpell(){
        super(SpellType.RESURRECT);
    }

    public int castSpell(int tileX, int tileY){
        BattleUnit unit = GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile();
        return unit.heal(GameManager.curPlayer()[0].getMagic() * HEALFORCE);
    }
}