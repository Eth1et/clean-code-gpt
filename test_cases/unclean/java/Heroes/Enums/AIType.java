package Heroes.Enums;

/**
 * Különböző ellenfél típusok felsorolása
 */
public enum AIType {
    LANDLORD,
    ELF,
    WIZARD,
    ARCHERMASTER;

    @Override
    public String toString(){
        switch(this){
            case ELF:
                return "Elf";
            case WIZARD:
                return "Varázsló";
            case LANDLORD:
                return "Földesúr";
            case ARCHERMASTER:
                return "Íjász Mester";
        }
        return "";
    }
}
