package prog1.kotprog.dontstarve.solution.character;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.character.actions.Action;
import prog1.kotprog.dontstarve.solution.character.actions.ActionNone;
import prog1.kotprog.dontstarve.solution.inventory.BaseInventory;
import prog1.kotprog.dontstarve.solution.inventory.Inventory;
import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.EquippableItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;
import prog1.kotprog.dontstarve.solution.inventory.items.Droppable;
import prog1.kotprog.dontstarve.solution.level.Field;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObject;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObjectType;
import prog1.kotprog.dontstarve.solution.utility.Direction;
import prog1.kotprog.dontstarve.solution.utility.Position;

/**
 * Egy karakter megvalósítása.
 */
public class GameCharacter implements BaseCharacter {
    /**
     * Egy karakter sebessége.
     */
    private final float speed;
    /**
     * Egy karakter éhsége.
     */
    private float hunger;
    /**
     * Egy karakter életereje.
     */
    private float hp;

    /**
     * Egy karakter maximális éhsége.
     */
    private final float maxHunger;
    /**
     * Egy karakter maximális életereje.
     */
    private final float maxHp;

    /**
     * A játékos eszköztára.
     */
    private final BaseInventory inventory;

    /**
     * Megadja, hogy a karaktert játékos irányítja-e.
     */
    private final boolean player;

    /**
     * A játékos pozíciója.
     */
    private Position currentPosition;

    /**
     * A játékos utolsó akciója.
     */
    private Action lastAction;

    /**
     * A játékos neve.
     */
    private final String name;

    /**
     * A karakter konstruktora.
     *
     * @param name     karakter neve
     * @param player   játékos-e az adott karakter
     * @param position a kezdőpozíció
     * @param hp       kezdő életerő
     * @param hunger   kezdő éhség
     * @param speed    kezdő sebesség
     */
    public GameCharacter(String name, boolean player, Position position, float hp, float hunger, float speed) {
        this.name = name;
        this.player = player;
        this.currentPosition = position;
        lastAction = new ActionNone();
        inventory = new Inventory();
        this.hp = hp;
        this.maxHp = hp;
        this.hunger = hunger;
        this.maxHunger = hunger;
        this.speed = speed;
    }

    /**
     * Megadja hogy van e a kezében tool és megfelelő típusú-e.
     * @param object az adott objektumhoz
     * @return boolean
     */
    private boolean hasRightToolForObject(InteractiveObject object){
        return inventory.equippedItem() != null && object.requiredToolType() == inventory.equippedItem().getType();
    }

    /**
     * Megadja, hogy az adott mezővel lehet e interaktálni.
     * @param field a mező
     * @return invalid-e
     */
    private boolean invalidField(Field field){
        return field == null || field.getInteractiveObject() == null || field.getInteractiveObject().getType() == InteractiveObjectType.FIRE;
    }

    /**
     * A karakter interaktál az adott mezőn lévő objektummal.
     *
     * @param field az adott mező
     * @return sikerült-e az interakció
     */
    public boolean interactWithField(Field field) {
        if (invalidField(field)) {
            return false;
        }
        if(hasRightToolForObject(field.getInteractiveObject())){
            if(inventory.equippedItem().decreaseDurability()){
                inventory.equippedItemBreaks();
            }
            if(!field.getInteractiveObject().takeHit(inventory.equippedItem().getType())){
                return true;
            }
        }else if(!field.getInteractiveObject().takeHit(null)){
            return true;
        }
        AbstractItem item = field.getInteractiveObject().gatherResource();
        field.destroyInteractiveObject();
        if (Droppable.dropsToGround(item.getType()) || !inventory.addItem(item)) {
            field.addItem(item);
        }
        return true;
    }

    /**
     * Végrehajtja az adott akciót, majd eltárolja.
     *
     * @param action az akció
     */
    public void executeAction(Action action) {
        lastAction = action.execute(this)? action : new ActionNone();
    }

    /**
     * A karakter éhesebb lesz.
     */
    public void getHungrier() {
        hunger = Math.max(0, Math.min(maxHunger, hunger - 0.4f));
        if (hunger < 0.001) {
            takeDamage(5);
        }
    }

    /**
     * Mozgatja a játékost az adott irányba, ha lehetséges.
     *
     * @param direction az irány
     * @return sikerült-e
     */
    public boolean moveTowards(Direction direction) {
        Position move = switch (direction) {
            case UP -> new Position(0, -1);
            case DOWN -> new Position(0, 1);
            case LEFT -> new Position(-1, 0);
            case RIGHT -> new Position(1, 0);
        };

        move.multiply(getSpeed());
        Position destination = getCurrentPosition().added(move);
        Field targetField = GameManager.getInstance().getFieldByPosition(destination);

        if (targetField != null && targetField.isWalkable()) {
            currentPosition = destination;
            return true;
        }
        return false;
    }

    /**
     * Megtámadja az adott ellenfelet.
     *
     * @param enemy az ellenfél
     */
    public void attack(GameCharacter enemy) {
        EquippableItem equippedItem = inventory.equippedItem();
        int damage = (equippedItem == null) ? 4 : switch (equippedItem.getType()) {
            case SPEAR -> 19;
            case AXE, PICKAXE -> 8;
            default -> 6; //TORCH
        };

        enemy.takeDamage(damage);

        if (equippedItem == null || equippedItem.getType() == ItemType.TORCH || !equippedItem.decreaseDurability()) {
            return;
        }
        inventory.equippedItemBreaks();
    }

    /**
     * A karakter sebzést kap.
     *
     * @param damage a kapott sebzés mennyisége
     */
    private void takeDamage(float damage) {
        hp = Math.max(0, Math.min(maxHp, hp - damage));
        if (hp == 0) {
            die();
        }
    }

    /**
     * A karakter meghal.
     */
    private void die() {
        Field f = GameManager.getInstance().getFieldByPosition(getCurrentPosition());
        if (f == null) {
            return;   //JUST TO SUPPRESS WARNING, shouldn't be an issue tho
        }
        if (inventory.equippedItem() != null) {
            f.addItem(inventory.unequipItem());
            inventory.equippedItemBreaks();
        }
        f.addItems(inventory.items());
    }

    /**
     * <b>hp</b> mennyiségű élet és <b>hunger</b> mennyiségű éhség feltöltése.
     *
     * @param hp     élet
     * @param hunger éhség
     */
    public void heal(int hp, int hunger) {
        this.hp = Math.min(maxHp, Math.max(0, this.hp + hp));
        this.hunger = Math.max(0, this.hunger + hunger);
    }

    /**
     * Játékos-e.
     *
     * @return Játékos-e a karakter
     */
    public boolean isPlayer() {
        return this.player;
    }

    /**
     * Megadja a sebesség szorzót a karakter életerejétől függően.
     * @param percent a karakter éhségi százaléka
     * @return a szorzó
     */
    private float getHealthMultiplierForSpeed(float percent){
        if (0 < percent && percent < 10) {
            return 0.6f;
        } else if (10 <= percent && percent < 30) {
            return 0.75f;
        } else if (30 <= percent && percent < 50) {
            return 0.9f;
        } else if (50 <= percent){
            return 1;
        }
        return 0;
    }

    /**
     * Megadja a sebesség szorzót a karakter éhségétől függően.
     * @param percent a karakter éhségi százaléka
     * @return a szorzó
     */
    private float getHungerMultiplierForSpeed(float percent){
        if (0 < percent && percent < 20) {
            return 0.8f;
        } else if (20 <= percent && percent < 50) {
            return 0.9f;
        } else if (50 <= percent){
            return 1;
        }
        return 0.5f;
    }

    /**
     * A karakter mozgási sebességének lekérdezésére szolgáló metódus.
     *
     * @return a karakter mozgási sebessége
     */
    public float getSpeed() {
        float percentHealth = hp / maxHp * 100;
        float percentHunger = hunger / maxHunger * 100;
        return this.speed * getHungerMultiplierForSpeed(percentHunger) * getHealthMultiplierForSpeed(percentHealth);
    }

    /**
     * A karakter jóllakottságának mértékének lekérdezésére szolgáló metódus.
     *
     * @return a karakter jóllakottsága
     */
    public float getHunger() {
        return this.hunger;
    }

    /**
     * A karakter életerejének lekérdezésére szolgáló metódus.
     *
     * @return a karakter életereje
     */
    public float getHp() {
        return this.hp;
    }

    /**
     * A karakter inventory-jának lekérdezésére szolgáló metódus.
     * <br>
     * A karakter inventory-ja végig ugyanaz marad, amelyet referencia szerint kell visszaadni.
     *
     * @return a karakter inventory-ja
     */
    public BaseInventory getInventory() {
        return this.inventory;
    }

    /**
     * A játékos aktuális pozíciójának lekérdezésére szolgáló metódus.
     *
     * @return a játékos pozíciója
     */
    public Position getCurrentPosition() {
        return this.currentPosition;
    }

    /**
     * Az utolsó cselekvés lekérdezésére szolgáló metódus.
     * <br>
     * Egy létező Action-nek kell lennie, nem lehet null.
     *
     * @return az utolsó cselekvés
     */
    public Action getLastAction() {
        return this.lastAction;
    }

    /**
     * A játékos nevének lekérdezésére szolgáló metódus.
     *
     * @return a játékos neve
     */
    public String getName() {
        return this.name;
    }
}
