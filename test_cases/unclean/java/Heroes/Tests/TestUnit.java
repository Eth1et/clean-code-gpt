package Heroes.Tests;

import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.Spells.Spell;
import Heroes.Units.Unit;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Teszteli a Unit osztály bizonyos metódusait
 */
public class TestUnit {
    @Test
    public void testUnitPrice(){
        assertEquals(2, Unit.getUnitPrice(UnitType.PEASANT));
        assertEquals(6, Unit.getUnitPrice(UnitType.ARCHER));
        assertEquals(15, Unit.getUnitPrice(UnitType.GRIFF));
        assertEquals(10, Unit.getUnitPrice(UnitType.KENTAUR));
        assertEquals(15, Unit.getUnitPrice(UnitType.GOLEM));
    }
    @Test
    public void testUnitHealth(){
        assertEquals(3, Unit.getUnitHealth(UnitType.PEASANT));
        assertEquals(7, Unit.getUnitHealth(UnitType.ARCHER));
        assertEquals(30, Unit.getUnitHealth(UnitType.GRIFF));
        assertEquals(10, Unit.getUnitHealth(UnitType.KENTAUR));
        assertEquals(43, Unit.getUnitHealth(UnitType.GOLEM));
    }
    @Test
    public void testUnitSpeed(){
        assertEquals(4, Unit.getUnitSpeed(UnitType.PEASANT));
        assertEquals(4, Unit.getUnitSpeed(UnitType.ARCHER));
        assertEquals(7, Unit.getUnitSpeed(UnitType.GRIFF));
        assertEquals(6, Unit.getUnitSpeed(UnitType.KENTAUR));
        assertEquals(5, Unit.getUnitSpeed(UnitType.GOLEM));
    }
}
