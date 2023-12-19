package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemStone;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;

/**
 * Egy mezőn lévő kő objektum.
 */
public class StoneObject extends InteractiveObject{

    /**
     * Stone Object inicializálása.
     */
    public StoneObject(){
        super(InteractiveObjectType.STONE, ItemType.PICKAXE, 5);
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return new ItemStone(3);
    }
}
