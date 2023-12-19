package Heroes.Enums;

/**
 * Egység típusok felsorolása
 */
public enum UnitType {
    PEASANT(0),
    ARCHER(1),
    GRIFF(2),
    KENTAUR(3),
    GOLEM(4);

    private final int value;
    private UnitType(int value){
        this.value = value;
    }

    public int getValue(){
        return value;
    }

    public String inHungarian(){
        switch(this){
            case PEASANT:
                return "Földműves";
            case ARCHER:
                return "Íjász";
            case GRIFF:
                return "Griff";
            case KENTAUR:
                return "Kentaúr";
            default:
                return "Gólem";
        }
    }
}
