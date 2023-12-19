package Heroes.Units;

import Heroes.Hero;

import java.util.List;
import java.util.Random;

/**
 * A csata során használt Egység fogalmat valósítja meg, vagyis egybefűzi a vásárolt egységeket,
 * tulajdonságaikat összegzi és megvalósítja a harcban használt funkciókat.
 */
public class BattleUnit {
    private int maxHealth;
    private List<Unit> units;
    private int freezed;
    private final Hero hero;
    private int x;
    private int y;
    private boolean backAttackedThisTurn;

    public boolean hasBackAttackedThisTurn(){
        return backAttackedThisTurn;
    }
    public int getFreezed() {
        return freezed;
    }
    public int getX() {
        return x;
    }
    public int getY() {
        return y;
    }
    public void setX(int x) {
        this.x = x;
    }
    public int getMaxHealth() {
        return maxHealth;
    }

    public void setY(int y) {
        this.y = y;
    }

    public Hero[] getHero() {
        return new Hero[]{hero};
    }
    public BattleUnit(List<Unit> units, Hero[] hero){
        this.units = units;
        maxHealth = units.size()*units.get(0).getHealth();
        freezed = 0;
        this.hero = hero[0];
        backAttackedThisTurn = false;
    }
    public void backAttackedThisTurn(){
        backAttackedThisTurn = true;
    }
    public void resetBackAttackedThisTurn(){
        backAttackedThisTurn = false;
    }
    public List<Unit> getUnits(){return units;}
    public int getUnitsAlive(){
        int c=0;
        for(Unit unit: units){
            if(unit.getHealth() > 0) c++;
        }
        return c;
    }
    public int getRndDamage(){
        Random rnd = new Random();
        return getUnitsAlive()*(units.get(0).getMinDamage() + rnd.nextInt(units.get(0).getMaxDamage()-units.get(0).getMinDamage()+1));
    }
    public int getHealth(){
        int s = 0;
        for(Unit unit: units){
            if(unit.getHealth() > 0){
                s += unit.getHealth();
            }
        }
        return s;
    }
    public int getSpeed() {return units.get(0).getSpeed();}
    public int getInitiative() {return units.get(0).getInitiative();}
    public int heal(int amount){
        int prev = getUnitsAlive();
        if(getHealth()!=0){
            for(Unit unit: units){
                int healedFor = Math.min(amount,Unit.getUnitHealth(unit.getUnitType()) - unit.getHealth());
                unit.setHealth(unit.getHealth()+healedFor);
                amount -= healedFor;
                if(amount <=0) break;
            }
        }
        return getUnitsAlive() - prev;
    }
    public int takeDamage(int damage){
        int prev = getUnitsAlive();
        for(Unit unit: units){
            int damagedFor = Math.min(damage,unit.getHealth());
            unit.setHealth(unit.getHealth()-damagedFor);
            damage-=damagedFor;
            if(damage <= 0) break;
        }
        return prev-getUnitsAlive();
    }
    public void setFreezed(){
        freezed = 2;
    }
    public boolean isFreezed(){return freezed > 0;}
    public void decreaseFrozenEffectDuration(){
        freezed = Math.max(0, freezed-1);
    }
}
