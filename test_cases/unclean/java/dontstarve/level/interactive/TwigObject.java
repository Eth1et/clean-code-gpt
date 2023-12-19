package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemTwig;

/**
 * Egy mezőn lévő gally objektum.
 */
public class TwigObject extends InteractiveObject{

    /**
     * Twig Object inicializálása.
     */
    public TwigObject(){
        super(InteractiveObjectType.TWIG, null, 2);
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return new ItemTwig(1);
    }
}
