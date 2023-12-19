package Heroes.Tests;

import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.GameManager;
import Heroes.Hero;
import Heroes.Spells.Spell;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Teszteli a Spell osztály bizonyos metódusait
 */
public class TestSpell {
    @Test
    public void testSpellGetCost(){
        assertEquals(60,Spell.getSpellCost(SpellType.LIGHTNINGSTRIKE));
        assertEquals(120,Spell.getSpellCost(SpellType.FIREBALL));
        assertEquals(120,Spell.getSpellCost(SpellType.RESURRECT));
        assertEquals(55,Spell.getSpellCost(SpellType.MAGICSHIELD));
        assertEquals(80,Spell.getSpellCost(SpellType.FREEZE));
    }
    @Test
    public void testSpellGetManaCost(){
        assertEquals(5,Spell.getSpellManaCost(SpellType.LIGHTNINGSTRIKE));
        assertEquals(9,Spell.getSpellManaCost(SpellType.FIREBALL));
        assertEquals(6,Spell.getSpellManaCost(SpellType.RESURRECT));
        assertEquals(7,Spell.getSpellManaCost(SpellType.MAGICSHIELD));
        assertEquals(9,Spell.getSpellManaCost(SpellType.FREEZE));
    }
    @Test
    public void testSpellGetArea(){
        assertEquals(0,Spell.getSpellArea(SpellType.LIGHTNINGSTRIKE));
        assertEquals(1,Spell.getSpellArea(SpellType.FIREBALL));
        assertEquals(0,Spell.getSpellArea(SpellType.RESURRECT));
        assertEquals(GameManager.width,Spell.getSpellArea(SpellType.MAGICSHIELD));
        assertEquals(0,Spell.getSpellArea(SpellType.FREEZE));
    }
}
