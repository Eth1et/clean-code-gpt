package prog1.kotprog.dontstarve.solution.level;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.level.interactive.FireObject;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObject;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObjectType;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Egy mezőt leíró osztály.
 */
public class Field implements BaseField{
    /**
     * Mezőn lévő Item-ek listája.
     */
    private final List<AbstractItem> itemsOnField;

    /**
     * Ráléphet e a játékos a mezőre.
     */
    private final boolean walkable;

    /**
     * A mezőn lévő interaktív objektum.
     * <br>null, ha nincs rajta semmi.
     */
    private InteractiveObject interactiveObject;

    /**
     * Egy mező konstruktora.
     */
    public Field(boolean walkable, InteractiveObject interactiveObject){
        this.walkable = walkable;
        this.interactiveObject = interactiveObject;
        itemsOnField = new ArrayList<>();
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mező járható-e.
     * @return igaz, amennyiben a mező járható; hamis egyébként
     */
    public boolean isWalkable(){
        return walkable;
    }

    /**
     * Megnézi, hogy az adott mezőn van- e type típusú interaktív objektum.
     * @param type a keresett típus
     * @return ha null, akkor hamis különben ha rajta van az adott objektum akkor igaz
     */
    private boolean checkInteractiveObjectType(InteractiveObjectType type){
        return interactiveObject != null && interactiveObject.getType() == type;
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e fa.
     * @return igaz, amennyiben van fa; hamis egyébként
     */
    public boolean hasTree(){
        return checkInteractiveObjectType(InteractiveObjectType.TREE);
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e kő.
     * @return igaz, amennyiben van kő; hamis egyébként
     */
    public boolean hasStone(){
        return checkInteractiveObjectType(InteractiveObjectType.STONE);
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e gally.
     * @return igaz, amennyiben van gally; hamis egyébként
     */
    public boolean hasTwig(){
        return checkInteractiveObjectType(InteractiveObjectType.TWIG);
    }

    /**
     * Ezen metódus segítségével lekérdezheő, hogy a mezőn van-e bogyó.
     * @return igaz, amennyiben van bogyó; hamis egyébként
     */
    public boolean hasBerry(){
        return checkInteractiveObjectType(InteractiveObjectType.BERRY);
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e répa.
     * @return igaz, amennyiben van répa; hamis egyébként
     */
    public boolean hasCarrot(){
        return checkInteractiveObjectType(InteractiveObjectType.CARROT);
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e tűz rakva.
     * @return igaz, amennyiben van tűz; hamis egyébként
     */
    public boolean hasFire(){
        return checkInteractiveObjectType(InteractiveObjectType.FIRE);
    }

    /**
     * Letesz az adott mezőre tábortüzet.
     */
    public void placeFire(){
        if(interactiveObject == null){
            interactiveObject = new FireObject();
        }
    }

    /**
     * Visszaadja az adott mező interaktív objektumát.
     * @return az objektum
     */
    public InteractiveObject getInteractiveObject(){
        return this.interactiveObject;
    }

    /**
     * Sets the interactive object to null.
     */
    public void destroyInteractiveObject(){
        this.interactiveObject = null;
    }

    /**
     * Ezen metódus segítségével a mezőn lévő tárgyak lekérdezhetők.<br>
     * A tömbben az a tárgy jön hamarabb, amelyik korábban került az adott mezőre.<br>
     * A karakter ha felvesz egy tárgyat, akkor a legkorábban a mezőre kerülő tárgyat fogja felvenni.<br>
     * Ha nem sikerül felvenni, akkor a (nem) felvett tárgy a tömb végére kerül.
     * @return a mezőn lévő tárgyak
     */
    public AbstractItem[] items(){
        return this.itemsOnField.toArray(new AbstractItem[itemsOnField.size()]);
    }

    /**
     * Kiveszi az adott indexű elemet a listából, ami tartalmazza a field-en lévő itemeket.
     * @param index az index
     * @return a kivett tárgy
     */
    public AbstractItem removeItem(int index){
        if(0 > index || index >= itemsOnField.size()){
            return null;
        }
        AbstractItem res = itemsOnField.get(index);
        itemsOnField.remove(index);
        return res;
    }

    /**
     * Ha van a mezőn tűz, akkor csökkenti az idejét, ha 0 akkor pedig törli.
     */
    public void decreaseFireTime(){
        if(hasFire() && interactiveObject.takeHit(null)){
            interactiveObject = null;
        }
    }

    /**
     * Hozzáadja az adott mezőhöz a tárgyat.
     * @param item a tárgy
     */
    public void addItem(AbstractItem item){
        itemsOnField.add(item);
    }

    /**
     * Hozzáadja az adott mezőhöz a tárgyakat.
     * @param items a tárgyak
     */
    public void addItems(AbstractItem[] items){
        this.itemsOnField.addAll(Arrays.stream(items).toList());
    }
}
