package Heroes.Tests;

import Heroes.Enums.UnitType;
import Heroes.Hero;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Teszteli a Hero osztály bizonyos metódusait
 */
public class TestHero {
    Hero h1,h2,h3;
    @BeforeEach
    public void setUp(){
        h1 = new Hero(false,100);
        h2 = new Hero(true,-100);
        h3 = new Hero(false,2424124);
    }

    @Test
    public void testConstructorAndBasicGetters(){

        assertEquals(100, h1.getMoney());
        assertFalse(h1.isPlayer());

        assertEquals(0, h2.getMoney());
        assertTrue(h2.isPlayer());

        assertEquals(2424124, h3.getMoney());
        assertFalse(h3.isPlayer());
    }

    @Test
    public void testSetAndDecreaseMagicShieldedEffectAndItsGetter(){

        assertEquals(0,h1.getMagicShielded());
        assertEquals(0,h2.getMagicShielded());
        assertEquals(0,h3.getMagicShielded());

        h1.setMagicShielded();
        h2.setMagicShielded();
        h3.setMagicShielded();

        assertEquals(2,h1.getMagicShielded());
        assertEquals(2,h2.getMagicShielded());
        assertEquals(2,h3.getMagicShielded());

        for(int i = 1; i <= 3; i++){
            h1.decreaseMagicShield();
            h2.decreaseMagicShield();
            h3.decreaseMagicShield();

            assertEquals(Math.max(0,2-i),h1.getMagicShielded());
            assertEquals(Math.max(0,2-i),h2.getMagicShielded());
            assertEquals(Math.max(0,2-i),h3.getMagicShielded());
        }
    }

    @Test
    public void testCountUnitsAndAddAndRemoveUnits(){
        assertEquals(0,h1.countUnits());
        assertEquals(0,h2.countUnits());
        assertEquals(0,h3.countUnits());

        for(int i = 0; i < 10; i++) h1.addUnit(UnitType.GRIFF);
        for(int i = 0; i < 2; i++) h2.addUnit(UnitType.GRIFF);
        for(int i = 0; i < 4; i++) h3.addUnit(UnitType.GRIFF);

        assertEquals(10,h1.countUnits());
        assertEquals(2,h2.countUnits());
        assertEquals(4,h3.countUnits());

        for(int i = 0; i < 2; i++) h1.removeUnit(UnitType.GRIFF);
        for(int i = 0; i < 1; i++) h2.removeUnit(UnitType.GRIFF);
        for(int i = 0; i < 2; i++) h3.removeUnit(UnitType.GRIFF);

        assertEquals(8,h1.countUnits());
        assertEquals(1,h2.countUnits());
        assertEquals(2,h3.countUnits());

        for(int i = 0; i < 200; i++) h1.removeUnit(UnitType.GRIFF);
        for(int i = 0; i < 200; i++) h2.removeUnit(UnitType.GRIFF);
        for(int i = 0; i < 200; i++) h3.removeUnit(UnitType.GRIFF);

        assertEquals(0,h1.countUnits());
        assertEquals(0,h2.countUnits());
        assertEquals(0,h3.countUnits());
    }
}
