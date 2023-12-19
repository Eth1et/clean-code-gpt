package Heroes;

import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.Spells.Spell;
import Heroes.Units.BattleUnit;
import Heroes.Units.Unit;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A Hős osztály az egymás ellen harcoló játékosokat valósítja meg.
 * Minden hős rendelkezik tulajdonságpontokkal és birtokolot egységekkel, képességekkel.
 * Emellett tud támadni is.
 */
public class Hero {
    private static final int DAMAGE=10;
    private int money;
    private final boolean isPlayer;
    private int attack;
    private int defense;
    private int magic;
    private int knowledge;
    private int moral;
    private int luck;
    private int magicShielded;
    private Map<UnitType,List<Unit>> units;
    private Map<SpellType,Boolean> availableSpells;
    private Map<UnitType, BattleUnit> battleUnits;
    private Map<SpellType,Spell> spells;
    private int mana;
    private int spellDelay;
    private int attackDelay;
    private boolean usedUnitThisTurn;

    public boolean isUsedUnitThisTurn() {
        return usedUnitThisTurn;
    }
    public Map<SpellType, Spell> getSpells() {
        return spells;
    }
    public int getAttackDelay() {
        return attackDelay;
    }
    public int getSpellDelay() {
        return spellDelay;
    }
    public int getMagicShielded() {
        return magicShielded;
    }
    public Map<UnitType, BattleUnit> getBattleUnits() {
        return battleUnits;
    }
    public Map<UnitType, List<Unit>> getUnits() {
        return units;
    }
    public Map<SpellType, Boolean> getAvailableSpells() {
        return availableSpells;
    }
    public boolean isPlayer() {
        return isPlayer;
    }
    public int getAttack() {
        return attack;
    }
    public int getDefense() {
        return defense;
    }
    public int getMagic() {
        return magic;
    }
    public int getKnowledge() {
        return knowledge;
    }
    public int getMoral() {
        return moral;
    }
    public int getMana() {
        return mana;
    }
    public int getLuck() {
        return luck;
    }
    public int getMoney() {return money;}
    public boolean isMagicShielded(){
        return magicShielded > 0;
    }

    public void setUsedUnitThisTurn(boolean usedUnitThisTurn) {
        this.usedUnitThisTurn = usedUnitThisTurn;
    }
    public void setAttackDelay(int attackDelay) {
        this.attackDelay = Math.max(0,attackDelay);
    }
    public void setSpellDelay(int spellDelay) {
        this.spellDelay = Math.max(0,spellDelay);
    }
    public void setMana(int mana) {
        this.mana = mana;
    }
    public void setAttack(int attack) {
        this.attack = Math.min(Math.max(1,attack),10);
    }
    public void setDefense(int defense) {
        this.defense = Math.min(Math.max(1,defense),10);
    }
    public void setMagic(int magic) {
        this.magic = Math.min(Math.max(1,magic),10);
    }
    public void setKnowledge(int knowledge) {
        this.knowledge = Math.min(Math.max(1,knowledge),10);
    }
    public void setMoral(int moral) {
        this.moral = Math.min(Math.max(1,moral),10);
    }
    public void setLuck(int luck) {
        this.luck = Math.min(Math.max(1,luck),10);
    }
    public void setMoney(int money) {this.money = Math.max(0, money);}

    public Hero(boolean isPlayer, int money) {
        this.isPlayer = isPlayer;
        setAttack(1);
        setDefense(1);
        setMagic(1);
        setKnowledge(1);
        setMoral(1);
        setLuck(1);
        setUpUnits();
        setUpAvailableSpells();
        setMoney(money);
        magicShielded = 0;
        spells = new HashMap<>(5);
    }

    /**
     * Megtámadja az adott mezőn lévő egységet.
     * @param x az egység x azaz magassági pozíciója a csatatéren.
     * @param y az egység Y azaz szélességi pozíciója a csatatéren.
     * @return a támadás eredményeképpen megölt egységek száma.
     */
    public int attackUnit(int x, int y){
        return GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().takeDamage(getAttack() * DAMAGE);
    }

    /**
     * Előkészíti a csata egységeket.
     */
    public void setUpBattleUnits(){
        battleUnits = new HashMap<>(UnitType.values().length);
        for(UnitType type: UnitType.values()){
            if(units.get(type).size()>0) battleUnits.put(type, new BattleUnit(units.get(type),new Hero[]{this}));
        }
    }
    private void setUpAvailableSpells(){
        availableSpells = new HashMap<>();
        for(SpellType type: SpellType.values()){
            availableSpells.put(type,false);
        }
    }
    private void setUpUnits(){
        units = new HashMap<>();
        for(UnitType type: UnitType.values()){
            units.put(type,new ArrayList<>());
        }
    }
    /**
     * Megszámolja hány egység van összesen.
     * @return a támadás eredményeképpen megölt egységek száma.
     */
    public int countUnits(){
        int sum = 0;
        for(UnitType type: UnitType.values()){
            sum+=units.get(type).size();
        }
        return sum;
    }
    /**
     * Hozzáad egy új egységet az egységekhez.
     * @param type az egység típusa.
     */
    public void addUnit(UnitType type){
        units.get(type).add(new Unit(type));
    }
    /**
     * Töröl egy egységet a megadott egységfajta közül.
     * @param type az egység típusa.
     */
    public void removeUnit(UnitType type){
        if(units.get(type).size() > 0){
            units.get(type).remove(units.get(type).size()-1);
        }
    }
    public void addSpell(SpellType type){
        availableSpells.replace(type, true);
        spells.put(type,Spell.getNewSpellBySpellType(type));
    }
    public void removeSpell(SpellType type){
        availableSpells.replace(type, false);
        spells.remove(type);
    }
    public void setMagicShielded(){
        magicShielded = 2;
    }
    public void decreaseMagicShield(){
        magicShielded = Math.max(0, magicShielded-1);
    }
    public boolean hasUnitWithLowHealth(){
        UnitType[] strongnessOrder = {UnitType.GRIFF,UnitType.GOLEM,UnitType.KENTAUR,UnitType.ARCHER,UnitType.PEASANT};
        for(UnitType type: strongnessOrder){
            if(battleUnits.containsKey(type) && (battleUnits.get(type).getHealth() <= battleUnits.get(type).getMaxHealth() * .3 && battleUnits.get(type).getHealth()!=0)){
                return true;
            }
        }
        return false;
    }
    public UnitType getUnitWithLowHealth(){
        UnitType[] strongnessOrder = {UnitType.GRIFF,UnitType.GOLEM,UnitType.KENTAUR,UnitType.ARCHER,UnitType.PEASANT};
        for(UnitType type: strongnessOrder){
            if(battleUnits.containsKey(type) && (battleUnits.get(type).getHealth() <= battleUnits.get(type).getMaxHealth() * .3 && battleUnits.get(type).getHealth()!=0)){
                return type;
            }
        }
        return null;
    }
    public UnitType getStrongestUnit(){
        UnitType stronk = null;
        int maxDMG = 0;
        for(UnitType type: UnitType.values()){
            if(battleUnits.containsKey(type) && battleUnits.get(type).getMaxHealth() > 0 &&
                    (battleUnits.get(type).getUnits().get(0).getMinDamage() + battleUnits.get(type).getUnits().get(0).getMaxDamage())/2 * battleUnits.get(type).getUnitsAlive() > maxDMG){
               stronk = type;
            }
        }
        return stronk;
    }
}
