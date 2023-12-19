package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemRawBerry;

/**
 * Egy mezőn lévő bogyóbokor objektum.
 */
public class BerryObject extends InteractiveObject{

    /**
     * Berry Object inicializálása.
     */
    public BerryObject(){
        super(InteractiveObjectType.BERRY, null, 1);
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return new ItemRawBerry(1);
    }
}
