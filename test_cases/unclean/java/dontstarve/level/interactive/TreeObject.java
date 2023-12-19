package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemLog;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;

/**
 * Egy mezőn lévő fa objektum.
 */
public class TreeObject extends InteractiveObject{

    /**
     * Tree Object inicializálása.
     */
    public TreeObject(){
        super(InteractiveObjectType.TREE, ItemType.AXE, 4);
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return new ItemLog(2);
    }
}
