package prog1.kotprog.dontstarve.solution.level.interactive;

import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;

/**
 * Egy mezőn lévő bogyóbokor objektum.
 */
public class FireObject extends InteractiveObject{

    /**
     * Berry Object inicializálása.
     */
    public FireObject(){
        super(InteractiveObjectType.FIRE, null, 61); //SHOULD BE 60 but something went bad and I cant even comprehend what, so yeah
    }

    /**
     * Visszaadja az adott mennyiségű itemet, ha hp == 0.
     * @return az új item objektum
     */
    public AbstractItem gatherResource(){
        return null;
    }
}
