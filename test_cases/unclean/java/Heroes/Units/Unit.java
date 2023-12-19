package Heroes.Units;

import Heroes.Enums.UnitType;

/**
 * Egyetlen egységet megvalósító osztály.
 */
public class Unit {
    private final UnitType unitType;
    private int health;
    private int speed;
    private int minDamage;
    private int maxDamage;
    private int initiative;

    public UnitType getUnitType() {
        return unitType;
    }
    public int getHealth() {
        return health;
    }
    public int getSpeed() {
        return speed;
    }
    public int getMinDamage() {
        return minDamage;
    }
    public int getMaxDamage() {
        return maxDamage;
    }
    public int getInitiative() {
        return initiative;
    }

    public void setHealth(int health) {
        this.health = health;
    }

    public Unit(UnitType unitType){
        this.unitType = unitType;
        this.health = getUnitHealth(unitType);
        this.speed = getUnitSpeed(unitType);
        this.minDamage = getUnitMinDamage(unitType);
        this.maxDamage = getUnitMaxDamage(unitType);
        this.initiative = getUnitInitiative(unitType);
    }

    public static int getUnitPrice(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 2;
            case ARCHER:
                return 6;
            case GRIFF:
                return 15;
            case KENTAUR:
                return 10;
            default:
                return 15;
        }
    }
    public static int getUnitMinDamage(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 1;
            case ARCHER:
                return 2;
            case GRIFF:
                return 4;
            case KENTAUR:
                return 3;
            default:
                return 4;
        }
    }
    public static int getUnitMaxDamage(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 1;
            case ARCHER:
                return 4;
            case GRIFF:
                return 6;
            case KENTAUR:
                return 5;
            default:
                return 5;
        }
    }
    public static int getUnitHealth(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 3;
            case ARCHER:
                return 7;
            case GRIFF:
                return 30;
            case KENTAUR:
                return 10;
            default:
                return 43;
        }
    }
    public static int getUnitSpeed(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 4;
            case ARCHER:
                return 4;
            case GRIFF:
                return 7;
            case KENTAUR:
                return 6;
            default:
                return 5;
        }
    }
    public static int getUnitInitiative(UnitType unitType){
        switch(unitType){
            case PEASANT:
                return 8;
            case ARCHER:
                return 9;
            case GRIFF:
                return 15;
            case KENTAUR:
                return 9;
            default:
                return 5;
        }
    }
}
