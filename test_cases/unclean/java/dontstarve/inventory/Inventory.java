package prog1.kotprog.dontstarve.solution.inventory;

import prog1.kotprog.dontstarve.solution.GameManager;
import prog1.kotprog.dontstarve.solution.inventory.items.EquippableItem;
import prog1.kotprog.dontstarve.solution.inventory.items.AbstractItem;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemType;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemCreator;
import prog1.kotprog.dontstarve.solution.inventory.items.FoodTester;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemRawCarrot;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemRawBerry;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemLog;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemTwig;
import prog1.kotprog.dontstarve.solution.inventory.items.ItemStone;
import prog1.kotprog.dontstarve.solution.level.Field;

import java.util.Map;


/**
 * Inventory megvalósítása.
 */
public class Inventory implements BaseInventory {

    /**
     * A karakter kezében lévő tárgy.
     */
    private EquippableItem itemInHand;

    /**
     * Inventoryban lévő tárgyak.
     */
    private final AbstractItem[] itemsInInventory;

    /**
     * Inventory objektum konstruktora.
     */
    public Inventory() {
        itemsInInventory = new AbstractItem[10];
        itemInHand = null;
    }

    /**
     * Egy item hozzáadása az inventory-hoz.<br>
     * Ha a hozzáadni kívánt tárgy halmozható, akkor a meglévő stack-be kerül (ha még fér, különben új stacket kezd),
     * egyébként a legelső új helyre kerül.<br>
     * Ha egy itemből van több megkezdett stack, akkor az inventory-ban hamarabb következőhöz adjuk hozzá
     * (ha esetleg ott nem fér el mind, akkor azt feltöltjük, és utána folytatjuk a többivel).<br>
     * Ha az adott itemből nem fér el mind az inventory-ban, akkor ami elfér azt adjuk hozzá, a többit pedig nem
     * (ebben az esetben a hívó félnek tudnia kell, hogy mennyit nem sikerült hozzáadni).
     *
     * @param item a hozzáadni kívánt tárgy
     * @return igaz, ha sikerült hozzáadni a tárgyat teljes egészében; hamis egyébként
     */
    public boolean addItem(AbstractItem item) {
        if(item == null){
            return false;
        }
        if(fillInventoryWithItem(item)){
            return true;
        }
        for (int i = 0; i < itemsInInventory.length; i++) {
            if (itemsInInventory[i] == null) {
                itemsInInventory[i] = ItemCreator.newItemByType(item.getType());
                itemsInInventory[i].setAmount(Math.min(item.getAmount(), itemsInInventory[i].getMaxAmount()));
                item.setAmount(item.getAmount() - itemsInInventory[i].getAmount());
                if (item.getAmount() == 0) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Segíti az addItem-et, feltölti az inventory már megkezdett slotjait az itemmel.
     * @param item az item
     * @return sikerült-e teljesen belerakni
     */
    private boolean fillInventoryWithItem(AbstractItem item){
        for (AbstractItem slot : itemsInInventory) {
            if (slot != null && slot.getType() == item.getType() && slot.getAmount() < slot.getMaxAmount()) {
                int freeRoom = slot.getMaxAmount() - slot.getAmount();
                if (freeRoom >= item.getAmount()) {
                    slot.setAmount(slot.getAmount() + item.getAmount());
                    item.setAmount(0);
                    return true;
                } else {
                    slot.setAmount(slot.getMaxAmount());
                    item.setAmount(item.getAmount() - freeRoom);
                }
            }
        }
        return false;
    }

    /**
     * Megnézi van-e elég resource, ha igen el is tünteti.
     * @param item az adott item lekraftolásához
     * @return sikerült-e
     */
    private boolean notEnoughResources(AbstractItem item){
        Map<ItemType, Integer> requirements = item.getRequiredResource();

        for (ItemType type : requirements.keySet()) {
            if (countAmount(type) < requirements.get(type)) {
                return true;
            }
        }

        for (ItemType type : requirements.keySet()) {
            removeItem(type, requirements.get(type));
        }

        return false;
    }

    /**
     * Létrehoz az adott típusú tárgyból 1-et.
     *
     * @param itemType a tárgy típusa
     * @return ha nem fért el az inventoryban vagy tábortűz, akkor item, különben null
     */
    public AbstractItem craftItem(ItemType itemType) {
        AbstractItem item = ItemCreator.newItemByType(itemType);

        if (!ItemType.craftable(item.getType()) || notEnoughResources(item)) {
            return null;
        }

        if (item.getType() == ItemType.FIRE || !addItem(item)) {
            return item;
        }
        return null;
    }

    /**
     * Egy tárgy kidobása az inventory-ból.
     * Hatására a tárgy eltűnik az inventory-ból.
     *
     * @param index a slot indexe, amelyen lévő itemet szeretnénk eldobni
     * @return az eldobott item
     */
    public AbstractItem dropItem(int index) {
        if (invalidIndex(index)) {
            return null;
        }
        AbstractItem ret = getItem(index);
        itemsInInventory[index] = null;
        return ret;
    }

    /**
     * Csökkenti a kézben lévő fáklya életét, ha van a kezében.
     */
    public void decreaseTorchDuration() {
        if (itemInHand != null && itemInHand.getType() == ItemType.TORCH && itemInHand.decreaseDurability()){
            equippedItemBreaks();
        }
    }

    /**
     * Bizonyos mennyiségű, adott típusú item törlése az inventory-ból. A törölt itemek véglegesen eltűnnek.<br>
     * Ha nincs elegendő mennyiség, akkor nem történik semmi.<br>
     * Az item törlése a legkorábban lévő stackből (stackekből) történik, akkor is, ha van másik megkezdett stack.<br>
     *
     * @param type   a törlendő item típusa
     * @param amount a törlendő item mennyisége
     * @return igaz, amennyiben a törlés sikeres volt
     */
    public boolean removeItem(ItemType type, int amount) {
        if (countAmount(type) < amount) {
            return false;
        }

        for (int i = 0; i < itemsInInventory.length; i++) {
            AbstractItem item = itemsInInventory[i];
            if (item != null && item.getType() == type) {
                int itemAmount = item.getAmount();
                item.setAmount(item.getAmount() - amount);  // Működik, mert az alsó korlátot vizsgáljuk a setAmount-ra
                if (item.getAmount() == 0) {
                    itemsInInventory[i] = null;
                }
                amount -= itemAmount - item.getAmount();
                if (amount <= 0) {
                    return true;
                }
            }
        }
        return true;
    }

    /**
     * Két item pozíciójának megcserélése az inventory-ban.<br>
     * Csak akkor használható, ha mind a két pozíción már van item.
     *
     * @param index1 a slot indexe, amelyen az első item található
     * @param index2 a slot indexe, amelyen a második item található
     * @return igaz, ha sikerült megcserélni a két tárgyat; hamis egyébként
     */
    public boolean swapItems(int index1, int index2) {
        if (invalidIndex(index1) || invalidIndex(index2) || getItem(index1) == null || getItem(index2) == null) {
            return false;
        }
        AbstractItem tmp = getItem(index1);
        itemsInInventory[index1] = itemsInInventory[index2];
        itemsInInventory[index2] = tmp;

        return true;
    }

    /**
     * Egy item átmozgatása az inventory egy másik pozíciójára.<br>
     * Csak akkor használható, ha az eredeti indexen van tárgy, az új indexen viszont nincs.
     *
     * @param index    a mozgatni kívánt item pozíciója az inventory-ban
     * @param newIndex az új pozíció, ahova mozgatni szeretnénk az itemet
     * @return igaz, ha sikerült a mozgatás; hamis egyébként
     */
    public boolean moveItem(int index, int newIndex) {
        if (invalidIndex(index) || invalidIndex(newIndex) || getItem(index) == null || getItem(newIndex) != null) {
            return false;
        }
        itemsInInventory[newIndex] = itemsInInventory[index];
        itemsInInventory[index] = null;

        return true;
    }

    /**
     * Két azonos típusú tárgy egyesítése.<br>
     * Csak stackelhető tárgyakra használható. Ha a két stack méretének összege a maximális stack méreten belül van,
     * akkor az egyesítés az első pozíción fog megtörténni. Ha nem, akkor az első pozíción lévő stack maximálisra
     * töltődik, a másikon pedig a maradék marad.<br>
     *
     * @param index1 első item pozíciója az inventory-ban
     * @param index2 második item pozíciója az inventory-ban
     * @return igaz, ha sikerült az egyesítés (változott valami a művelet hatására)
     */
    public boolean combineItems(int index1, int index2) {
        if (invalidIndex(index1) || invalidIndex(index2) || getItem(index1) == null
                || getItem(index2) == null || getItem(index1).getType() != getItem(index2).getType()
                || getItem(index1).getAmount() == getItem(index1).getMaxAmount()) {
            return false;
        }
        int sum = getItem(index1).getAmount() + getItem(index2).getAmount();

        if (sum > getItem(index1).getMaxAmount()) {
            getItem(index1).setAmount(getItem(index1).getMaxAmount());
            getItem(index2).setAmount(sum - getItem(index2).getMaxAmount());
        } else {
            getItem(index1).setAmount(sum);
            itemsInInventory[index2] = null;
        }

        return true;
    }

    /**
     * Egy item felvétele a karakter kezébe.<br>
     * Csak felvehető tárgyra használható. Ilyenkor az adott item a karakter kezébe kerül.
     * Ha a karakternek már tele volt a keze, akkor a kezében lévő item a most felvett item helyére kerül
     * (tehát gyakorlatilag helyet cserélnek).
     *
     * @param index a kézbe venni kívánt tárgy pozíciója az inventory-ban
     * @return igaz, amennyiben az itemet sikerült a kezünkbe venni
     */
    public boolean equipItem(int index) {
        if (invalidIndex(index) || !(getItem(index) instanceof EquippableItem)) {
            return false;
        }

        EquippableItem tmp = itemInHand;
        itemInHand = (EquippableItem) getItem(index);
        itemsInInventory[index] = tmp;

        return true;
    }

    /**
     * Null-ra állítja a kézben lévő eszközt.
     */
    public void equippedItemBreaks() {
        itemInHand = null;
    }

    /**
     * A karakter kezében lévő tárgy inventory-ba helyezése.<br>
     * A karakter kezében lévő item az inventory első szabad pozíciójára kerül.
     * Ha a karakternek üres volt a keze, akkor nem történik semmi.<br>
     * Ha nincs az inventory-ban hely, akkor a levett item a pálya azon mezőjére kerül, ahol a karakter állt.
     *
     * @return a levetett item, amennyiben az nem fért el az inventory-ban; null egyébként
     */
    public EquippableItem unequipItem() {
        if (itemInHand == null) {
            return null;
        }
        if (emptySlots() == 0) {
            EquippableItem tmp = itemInHand;
            itemInHand = null;
            return tmp;
        }
        for (int i = 0; i < itemsInInventory.length; i++) {
            if (itemsInInventory[i] == null) {
                EquippableItem tmp = itemInHand;
                itemInHand = null;
                itemsInInventory[i] = tmp;
                return null;
            }
        }
        return null;
    }

    /**
     * Begyűjti az adott mezőn lévő tárgyak közül a legelsőt.
     *
     * @param field a mező
     */
    public void collectItem(Field field) {
        if(field == null){
            return;
        }
        AbstractItem item = field.removeItem(0);
        if (item != null && !addItem(item)) {
            field.addItem(item);
        }
    }

    /**
     * Csökkenti az adott indexen lévő étel mennyiségét eggyel.
     *
     * @param index az index
     * @return a csökkentett étel típusa
     */
    private ItemType decreaseFoodAmount(int index) {
        if (invalidIndex(index) || getItem(index) == null || !FoodTester.isFood(getItem(index).getType())) {
            return null;
        }
        getItem(index).setAmount(getItem(index).getAmount() - 1);
        ItemType type = getItem(index).getType();

        if (getItem(index).getAmount() == 0) {
            itemsInInventory[index] = null;
        }
        return type;
    }

    /**
     * Egy item megfőzése.<br>
     * Csak nyers étel főzhető meg. Hatására az inventory adott pozíciójáról 1 egységnyi eltűnik.
     *
     * @param index A megfőzni kívánt item pozíciója az inventory-ban
     * @return A megfőzni kívánt item típusa
     */
    public ItemType cookItem(int index) {
        if (invalidIndex(index) || (!(getItem(index) instanceof ItemRawBerry) && !(getItem(index) instanceof ItemRawCarrot))) {
            return null;
        }

        return decreaseFoodAmount(index);
    }

    /**
     * Egy item elfogyasztása.<br>
     * Csak ételek ehetők meg. Hatására az inventory adott pozíciójáról 1 egységnyi eltűnik.
     *
     * @param index A megenni kívánt item pozíciója az inventory-ban
     * @return A megenni kívánt item típusa
     */
    public ItemType eatItem(int index) {
        return decreaseFoodAmount(index);
    }

    /**
     * A rendelkezésre álló üres inventory slotok számának lekérdezése.
     *
     * @return az üres inventory slotok száma
     */
    public int emptySlots() {
        int c = 0;
        for (AbstractItem item : itemsInInventory) {
            if (item == null) {
                c++;
            }
        }
        return c;
    }

    /**
     * Az aktuálisan viselt tárgy lekérdezése.<br>
     * Ha a karakter jelenleg egy tárgyat sem visel, akkor null.<br>
     *
     * @return Az aktuálisan viselt tárgy
     */
    public EquippableItem equippedItem() {
        return this.itemInHand;
    }

    /**
     * Adott inventory sloton lévő tárgy lekérdezése.<br>
     * Az inventory-ban lévő legelső item indexe 0, a következőé 1, és így tovább.<br>
     * Ha az adott pozíció üres, akkor null.<br>
     *
     * @param index a lekérdezni kívánt pozíció
     * @return az adott sloton lévő tárgy
     */
    public AbstractItem getItem(int index) {
        if (invalidIndex(index)) {
            return null;
        }
        return itemsInInventory[index];
    }

    /**
     * Megszámolja hány darab van az adott típusú tárgyból az inventoryban.
     *
     * @param type típus
     * @return összesen mennyi van
     */
    private int countAmount(ItemType type) {
        int c = 0;
        for (AbstractItem item : itemsInInventory) {
            if (item != null && item.getType() == type) {
                c += item.getAmount();
            }
        }
        return c;
    }

    /**
     * Visszaadja a teljes inventory tartalmát.
     *
     * @return a tartalom
     */
    public AbstractItem[] items() {
        AbstractItem[] res = new AbstractItem[itemsInInventory.length - emptySlots()];
        int i = 0;
        for (int j = 0; j < itemsInInventory.length; j++) {
            if (itemsInInventory[j] != null) {
                res[i] = dropItem(j);
                i++;
            }
        }
        return res;
    }

    /**
     * Csatlakozás után a csatlakozó karakter kap 4 darab véletlenszer¶ alap nyersanyagot (fa, kő, gally, bogyó, répa).
     */
    public void giveStarterLoot() {
        for (int i = 0; i < 4; i++) {
            AbstractItem item = switch (GameManager.getInstance().getRandom().nextInt(1, 6)) {
                case 1 -> new ItemLog(1);
                case 2 -> new ItemStone(1);
                case 3 -> new ItemTwig(1);
                case 4 -> new ItemRawBerry(1);
                default -> new ItemRawCarrot(1);
            };

            addItem(item);
        }
    }

    /**
     * Megmondja, hogy megfelelő index-e.
     *
     * @param index az ellenőrzött index
     * @return megfelelő-e
     */
    private boolean invalidIndex(int index) {
        return 0 > index || index >= itemsInInventory.length;
    }

    /**
     * Megadja, hogy van-e kajánk.
     * @return a legelső kaja indexe, vagy -1
     */
    public int hasFood(){
        for(int i = 0; i < itemsInInventory.length; i++){
            if(itemsInInventory[i] != null && FoodTester.isFood(itemsInInventory[i].getType())){
                return i;
            }
        }
        return -1;
    }
}
