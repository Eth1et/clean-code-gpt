package Heroes.Spells;

import Heroes.Enums.SpellType;
import Heroes.GameManager;

/**
 * Absztrakt osztály a képességek általános leírására.
 * Emellett metaadatokkal szolgál a kért képesség típusról.
 */
public abstract class Spell {
    private SpellType spellType;
    private int cost;
    private int manaCost;

    public Spell(SpellType spellType){
        this.spellType = spellType;
        this.cost = getSpellCost(spellType);
        this.manaCost = getSpellManaCost(spellType);
    }

    public static int getSpellCost(SpellType spellType){
        switch(spellType){
            case LIGHTNINGSTRIKE:
                return  60;
            case FIREBALL:
                return  120;
            case RESURRECT:
                return  120;
            case MAGICSHIELD:
                return 55;
            case FREEZE:
                return  80;
        }
        return 0;
    }
    public static int getSpellManaCost(SpellType spellType){
        switch(spellType){
            case LIGHTNINGSTRIKE:
                return  5;
            case FIREBALL:
                return  9;
            case RESURRECT:
                return  6;
            case MAGICSHIELD:
                return 7;
            case FREEZE:
                return  9;
        }
        return 0;
    }
    public static int getSpellArea(SpellType spellType){
        switch(spellType){
            case FIREBALL:
                return  1;
            case MAGICSHIELD:
                return GameManager.width;
            default:
                return  0;
        }
    }
    public static Spell getNewSpellBySpellType(SpellType spellType){
        switch (spellType){
            case FREEZE:
                return new FreezeSpell();
            case FIREBALL:
                return new FireBallSpell();
            case RESURRECT:
                return new ResurrectSpell();
            case MAGICSHIELD:
                return new MagicShieldSpell();
            case LIGHTNINGSTRIKE:
                return new LightningStrikeSpell();
        }
        return null;
    }
    public abstract int castSpell(int tileX, int tileY);
}
