package Heroes.Enums;

/**
 * Képesség típusok felsorolása
 */
public enum SpellType{
    LIGHTNINGSTRIKE,
    FIREBALL,
    RESURRECT,
    MAGICSHIELD,
    FREEZE;

    public String inHungarian(){
        switch(this){
            case LIGHTNINGSTRIKE:
                return "Villámcsapás";
            case FIREBALL:
                return "Tűzgolyó";
            case RESURRECT:
                return "Feltámasztás";
            case MAGICSHIELD:
                return "Varázspajzs";
            default:
                return "Fagyasztás";
        }
    }
}
