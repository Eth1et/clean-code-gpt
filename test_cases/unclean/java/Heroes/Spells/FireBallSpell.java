package Heroes.Spells;

import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.GameManager;
import Heroes.Units.BattleUnit;

/**
 * A képesség specializálása, a Tűzgolyó támadás működését valósítja meg.
 */
public class FireBallSpell extends Spell {
    private static final int DAMAGE = 20;

    public FireBallSpell(){
        super(SpellType.FIREBALL);
    }

    public int castSpell(int tileX, int tileY){
        int died = 0;
        int area = Spell.getSpellArea(SpellType.FIREBALL);
        int startY = Math.max(tileY-area,0);
        int endY = Math.min(tileY+area,GameManager.width-1);
        int startX = Math.max(tileX-area,0);
        int endX = Math.min(tileX+area,GameManager.height-1);
        for(int i = startX; i <= endX; i++){
            for(int j = startY; j <= endY; j++){
                BattleUnit unit = GameManager.getBattleField().getTiles()[i][j].getUnitOnTile();
                if(unit != null && unit.getUnits().get(0).getUnitType()!= UnitType.GOLEM) {
                    died += unit.takeDamage(GameManager.curPlayer()[0].getMagic() * DAMAGE);
                    if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHealth() <= 0){
                        GameManager.getBattleField().getTiles()[i][j].removeUnitFromTile();
                    }
                }
            }
        }
        return died;
    }
}
