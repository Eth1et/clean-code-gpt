package Heroes.Spells;

import Heroes.Enums.SpellType;
import Heroes.GameManager;
import Heroes.Units.BattleUnit;

/**
 * A képesség specializálása, a Villámcsapás támadás működését valósítja meg.
 */
public class LightningStrikeSpell extends Spell{
    private static final int DAMAGE = 30;

    public LightningStrikeSpell(){
        super(SpellType.LIGHTNINGSTRIKE);
    }

    public int castSpell(int tileX, int tileY){
        BattleUnit unit = GameManager.getBattleField().getTiles()[tileX][tileY].getUnitOnTile();
        return unit.takeDamage(GameManager.curPlayer()[0].getMagic() * DAMAGE);
    }
}
