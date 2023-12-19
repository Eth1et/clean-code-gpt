package prog1.kotprog.dontstarve.solution.utility;

/**
 * Egy 2 dimenziós (x, y) koordinátát leíró osztály.
 */
public class Position {

    /**
     * vízszintes (x) irányú koordináta.
     */
    private float x;

    /**
     * függőleges (y) irányú koordináta.
     */
    private float y;

    /**
     * Két paraméteres konstruktor, amely segítségével egy új pozíciót lehet létrehozni.
     *
     * @param x vízszintes (x) irányú koordináta
     * @param y függőleges (y) irányú koordináta
     */
    public Position(float x, float y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Házzad egy pozíciót és visszaadja eredményként ( nem változtatja az adott objektum értékét ).
     *
     * @param position a hozzáadni kívánt pozíció
     * @return a pozíciók komponensenkénti összege
     */
    public Position added(Position position) {
        return new Position(x + position.getX(), y + position.getY());
    }


    /**
     * Megszorozza a pozíció mindkét komponensét az adott súllyal.
     *
     * @param weight a súly
     */
    public void multiply(float weight) {
        x *= weight;
        y *= weight;
    }

    /**
     * Az aktuális koordinátához legközelebbi, csak egész értékű komponensekből álló koordináta kiszámítása.<br>
     * A kerekítés a matematika szabályainak megfelelően történik.
     *
     * @return a kiszámolt pozíció
     */
    public Position getNearestWholePosition() {
        return new Position(Math.round(this.x), Math.round(this.y));
    }

    /**
     * Megadja egy másik ponttól vett távolságot.
     *
     * @param other a másik pozíció
     * @return a távolság float-ként
     */
    public float distanceToPoint(Position other) {
        return (float) Math.sqrt(Math.pow(other.getX() - x, 2) + Math.pow(other.getY() - y, 2));
    }

    /**
     * x koordináta gettere.
     *
     * @return x koordináta
     */
    public float getX() {
        return x;
    }

    /**
     * y koordináta gettere.
     *
     * @return y koordináta
     */
    public float getY() {
        return y;
    }

    /**
     * x koordináta settere.
     *
     * @param x új x érték
     */
    public void setX(float x) {
        this.x = x;
    }

    /**
     * y koordináta settere.
     *
     * @param y új y érték
     */
    public void setY(float y) {
        this.y = y;
    }

    /**
     * Megadja, hogy megegyező koordinátára mutatnak-e.
     * @param other a másik pont
     * @return boolean
     */
    public boolean equals(Position other){
        return x == other.getX() && y == other.getY();
    }
}
