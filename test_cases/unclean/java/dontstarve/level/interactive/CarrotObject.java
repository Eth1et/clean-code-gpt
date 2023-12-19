package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemRawCarrot;

/**
 * Egy mezőn lévő répa objektum.
 */
public class CarrotObject extends InteractiveObject{

    /**
     * Carrot Object inicializálása.
     */
    public CarrotObject(){
        super(InteractiveObjectType.CARROT, null, 1);
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return new ItemRawCarrot(1);
    }
}
