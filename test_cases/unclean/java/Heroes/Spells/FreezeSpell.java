package Heroes.Spells;

import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.GameManager;
import Heroes.Units.BattleUnit;

/**
 * A képesség specializálása, a Fagyasztás képesség működését valósítja meg.
 */
public class FreezeSpell extends Spell{
    public static final int DAMAGE = 20;

    public FreezeSpell( ){
        super(SpellType.FREEZE);
    }

    public int castSpell(int tileX, int tileY){
        GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile().setFreezed();
        if(GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile().getUnits().get(0).getUnitType()== UnitType.GOLEM){
            GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile().takeDamage(GameManager.curPlayer()[0].getMagic() * DAMAGE);
        }
        return GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile().getFreezed();
    }
}
