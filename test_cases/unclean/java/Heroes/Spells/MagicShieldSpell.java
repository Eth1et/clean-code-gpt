package Heroes.Spells;

import Heroes.Enums.BattleStage;
import Heroes.Enums.SpellType;
import Heroes.GameManager;

/**
 * A képesség specializálása, a Varázspajzs varázslat működését valósítja meg.
 */
public class MagicShieldSpell extends Spell{
    public MagicShieldSpell(){
        super(SpellType.MAGICSHIELD);
    }

    public int castSpell(int tileX, int tileY){
        if(GameManager.getBattleStage() == BattleStage.P1ROUND){
            GameManager.getPlayerOne()[0].setMagicShielded();
            return GameManager.getPlayerOne()[0].getMagicShielded();
        }else{
            GameManager.getPlayerTwo()[0].setMagicShielded();
            return GameManager.getPlayerTwo()[0].getMagicShielded();
        }
    }
}
