package prog1.kotprog.dontstarve.solution.level;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObject;

/**
 * A pálya egy általános mezőjét leíró interface.
 */
public interface BaseField {
    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mező járható-e.
     * @return igaz, amennyiben a mező járható; hamis egyébként
     */
    boolean isWalkable();

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e fa.
     * @return igaz, amennyiben van fa; hamis egyébként
     */
    boolean hasTree();

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e kő.
     * @return igaz, amennyiben van kő; hamis egyébként
     */
    boolean hasStone();

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e gally.
     * @return igaz, amennyiben van gally; hamis egyébként
     */
    boolean hasTwig();

    /**
     * Ezen metódus segítségével lekérdezheő, hogy a mezőn van-e bogyó.
     * @return igaz, amennyiben van bogyó; hamis egyébként
     */
    boolean hasBerry();

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e répa.
     * @return igaz, amennyiben van répa; hamis egyébként
     */
    boolean hasCarrot();

    /**
     * Ezen metódus segítségével lekérdezhető, hogy a mezőn van-e tűz rakva.
     * @return igaz, amennyiben van tűz; hamis egyébként
     */
    boolean hasFire();

    /**
     * Letesz az adott mezőre tábortüzet.
     */
    void placeFire();

    /**
     * Visszaadja az adott mező interaktív objektumát.
     * @return az objektum
     */
    InteractiveObject getInteractiveObject();

    /**
     * Sets the interactive object to null.
     */
    void destroyInteractiveObject();

    /**
     * Kiveszi az adott indexű elemet a listából, ami tartalmazza a field-en lévő itemeket.
     * @param index az index
     * @return a kivett tárgy
     */
    AbstractItem removeItem(int index);

    /**
     * Ha van a mezőn tűz, akkor csökkenti az idejét, ha 0 akkor pedig törli.
     */
    void decreaseFireTime();

    /**
     * Hozzáadja az adott mezőhöz a tárgyat.
     * @param item a tárgy
     */
    void addItem(AbstractItem item);

    /**
     * Hozzáadja az adott mezőhöz a tárgyakat.
     * @param items a tárgyak
     */
    void addItems(AbstractItem[] items);

    /**
     * Ezen metódus segítségével a mezőn lévő tárgyak lekérdezhetők.<br>
     * A tömbben az a tárgy jön hamarabb, amelyik korábban került az adott mezőre.<br>
     * A karakter ha felvesz egy tárgyat, akkor a legkorábban a mezőre kerülő tárgyat fogja felvenni.<br>
     * Ha nem sikerül felvenni, akkor a (nem) felvett tárgy a tömb végére kerül.
     * @return a mezőn lévő tárgyak
     */
    AbstractItem[] items();
}
