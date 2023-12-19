package Heroes;

import Heroes.Enums.*;
import Heroes.Spells.Spell;
import Heroes.Units.BattleUnit;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

/**
 * A GameManager egy nem példányosítható osztály, amely a játék alap mechanikáit valósítja meg, hajtja végre.
 * A játék állásáról adatokat tárol.
 */
public final class GameManager {
    private static Hero playerOne;
    private static Hero playerTwo;
    private static boolean isPVP;
    private static AIType aiType;
    private static int round;
    private static int curUnitID;
    private static SpellType selectedSpellType;

    private static List<BattleUnit> queueUnits;

    public static final int width = 12, height = 10,startAvailableCols = 2;
    private static BattleStage battleStage;
    private static BattleField battleField;
    private static UnitType selectedUnitType;
    private static BattleField.Tile selectedTile;

    public static SpellType getSelectedSpellType(){return selectedSpellType;}
    public static void setSelectedSpellType(SpellType spellType){
        selectedSpellType=spellType;
    }
    public static int getRound() {
        return round;
    }
    public static List<BattleUnit> getQueueUnits() {
        return queueUnits;
    }
    public static BattleField getBattleField() {
        return battleField;
    }
    public static BattleField.Tile getSelectedTile() {
        return selectedTile;
    }
    public static void setSelectedTile(BattleField.Tile targetTile) {
        if(targetTile == null || targetTile.isAvailable()){
            selectedTile = targetTile;
            if(targetTile!=null) {
                selectedTile.setTileSelected();
                for(BattleField.Tile[] row: battleField.getTiles()){
                    for(BattleField.Tile tile : row){
                        if(tile.getX() != targetTile.getX() || tile.getY() != targetTile.getY()){
                            tile.disselectTile();
                        }
                    }
                }
            }
        }
    }
    public static UnitType getSelectedUnitType() {
        return selectedUnitType;
    }
    public static void setSelectedUnitType(UnitType type) {selectedUnitType = type;}
    public static void setBattleField(BattleField battleField){
        GameManager.battleField = battleField;
    }
    public static void setBattleStage(BattleStage battleStage) {
        GameManager.battleStage = battleStage;
    }
    public static BattleStage getBattleStage() {
        return battleStage;
    }
    public static void setAiType(AIType aiType) {
        GameManager.aiType = aiType;
    }
    public static AIType getAiType() {
        return aiType;
    }
    public static boolean isIsPVP() {
        return isPVP;
    }
    public static void setIsPVP(boolean isPVP) {
        GameManager.isPVP = isPVP;
    }
    public static Hero[] getPlayerOne() {
        return new Hero[] {playerOne};
    }
    public static Hero[] getPlayerTwo() {
        return new Hero[] {playerTwo};
    }
    public static void setUpMana(){
        playerOne.setMana(playerOne.getKnowledge()*10);
        playerTwo.setMana(playerTwo.getKnowledge()*10);
    }
    /**
     * Megadja, hogy bizonyos nehézségi fokozaton mennyi kezdőpénzt kap a játékos.
     * @param difficulty a nehézségi fokozat, amin játszik
     * @return az ennek megfelelő kezdőpénz egész számként
     */
    public static int difficultyBasedMoney(Difficulty difficulty){
        switch (difficulty){
            case EASY:
                return 1300;
            case MEDIUM:
                return 1000;
            default:
                return 700;
        }
    }

    public static void initialize(Difficulty difficulty){
        if(isPVP){
            playerOne = new Hero(true, difficultyBasedMoney(difficulty));
            playerTwo = new Hero(true, difficultyBasedMoney(difficulty));
        }else{
            playerOne = new Hero(true, difficultyBasedMoney(difficulty));
            playerTwo = new Hero(false, 1000);
        }
        battleStage = BattleStage.PREGAME;
        setSelectedUnitType(null);
        selectedTile = null;
        initializeQueue();
    }
    /**
     * Felkészíti a sorrend listát az egységek hozzáadásához. Feltölti null elemekkel.
     */
    private static void initializeQueue(){
        queueUnits = new ArrayList<>(10);
        for(int i = 0; i < 10; i++){
            queueUnits.add(null);
        }
    }
    public static void resetAI(){
        if(!isPVP){
            playerTwo = new Hero(false, 1000);
        }
    }
    public static int castSpell(SpellType type, int row, int col){
        curPlayer()[0].setSpellDelay(1);
        curPlayer()[0].setAttackDelay(1);
        curPlayer()[0].setMana(curPlayer()[0].getMana()-Spell.getSpellManaCost(type));
        return curPlayer()[0].getSpells().get(type).castSpell(row, col);
    }
    public static int heroAttack(int x, int y){
        if(curPlayer()[0].getAttackDelay() == 0){
            curPlayer()[0].setSpellDelay(1);
            curPlayer()[0].setAttackDelay(1);
            return curPlayer()[0].attackUnit(x,y);
        }
        return 0;
    }
    // 0 = nem | 1 = gyozelem | 2 = vereseg | 3 = dontetlen
    public static int checkForGameOver(){
        int p1h = 0; int p2h = 0;
        for(UnitType unitType: UnitType.values()){
            if(playerOne.getBattleUnits().containsKey(unitType)){
                p1h += playerOne.getBattleUnits().get(unitType).getHealth();
            }
            if(playerTwo.getBattleUnits().containsKey(unitType)){
                p2h += playerTwo.getBattleUnits().get(unitType).getHealth();
            }
        }
        if(p1h > 0 && p2h > 0){
            return 0;
        }else{
            battleStage = BattleStage.GAMEOVER;
            if(p1h > 0) {
                return 1;
            }else if( p2h > 0) {
                return 2;
            }else{
                return 3;
            }
        }
    }
    private static int[] attackUnit(int x, int y){
        int[] ret = {0,0};
        double baseDamage = GameManager.curPlayer()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).getRndDamage();
        baseDamage *= (1 + (.1 * GameManager.curPlayer()[0].getAttack()));
        Hero enemy = GameManager.getBattleStage() == BattleStage.P1ROUND ? GameManager.getPlayerOne()[0] : GameManager.getPlayerTwo()[0];
        baseDamage *= (1 - (enemy.getDefense() * .05));
        int damage = (int) Math.floor(baseDamage);
        Random rnd = new Random();
        if (rnd.nextFloat() <= (GameManager.curPlayer()[0].getLuck() * .05)) {
            damage *= 2;
            ret[1] = 1;
        }
        ret[0] = GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().takeDamage(damage);
        return ret;
    }
    public static int[] unitAttackUnit(int x, int y){
        int[] ret = new int[] { -1, -1, -1, -1};
        int[] tmp = attackUnit(x, y);
        ret[0] = tmp[0];
        ret[2] = tmp[1];
        Hero enemy = curEnemy()[0];
        if(curPlayer()[0].getBattleUnits().get(getQueueUnits().get(0).getUnits().get(0).getUnitType()).getUnits().get(0).getUnitType() != UnitType.KENTAUR &&
                enemy.getBattleUnits().get(getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType()).getHealth() > 0 &&
                (!enemy.getBattleUnits().get(getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType()).hasBackAttackedThisTurn() ||
                        getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType() == UnitType.GRIFF )){
            if((queueUnits.get(0).getUnits().get(0).getUnitType()!=UnitType.ARCHER || (queueUnits.get(0).getUnits().get(0).getUnitType()==UnitType.ARCHER
                    && GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType() == UnitType.ARCHER))
                    && !enemy.getBattleUnits().get(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType()).isFreezed()
            ){
                if((queueUnits.get(0).getUnits().get(0).getUnitType() != UnitType.ARCHER && battleField.getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType() != UnitType.ARCHER)
                        || queueUnits.get(0).getUnits().get(0).getUnitType() == UnitType.ARCHER && battleField.getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType() == UnitType.ARCHER){
                    tmp = backAttack(x, y);
                    ret[1] = tmp[0];
                    ret[3] = tmp[1];
                }
            }
        }
        return ret;
    }
    private static int[] backAttack(int x, int y){
        int[] ret = {0,0};
        double baseDamage = curEnemy()[0].getBattleUnits().get(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType()).getRndDamage();
        baseDamage *= (1 + (.1 * curEnemy()[0].getAttack()));

        baseDamage *= (1 - (curPlayer()[0].getDefense() * .05));
        Random rnd = new Random();
        if (rnd.nextFloat() <= (curEnemy()[0].getLuck() * .05)) {
            baseDamage *= 2;
            ret[1] = 1;
        }
        baseDamage *= 0.5;
        int damage = (int) Math.floor(baseDamage);
        curEnemy()[0].getBattleUnits().get(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType()).backAttackedThisTurn();
        ret[0] = curPlayer()[0].getBattleUnits().get(queueUnits.get(0).getUnits().get(0).getUnitType()).takeDamage(damage);
        return ret;
    }
    public static void resetBackAttacks(){
        for(UnitType type : UnitType.values()){
            if(playerOne.getBattleUnits() != null &&playerOne.getBattleUnits().containsKey(type)) playerOne.getBattleUnits().get(type).resetBackAttackedThisTurn();
            if(playerTwo.getBattleUnits() != null && playerTwo.getBattleUnits().containsKey(type)) playerTwo.getBattleUnits().get(type).resetBackAttackedThisTurn();
        }
    }
    public static void selectedSpell(){
        clearTiles();
    }
    public static void nextBattleStage(){
        switch (battleStage){
            case PREGAME:
                battleStage = BattleStage.P1TACTICAL;
                setAvailableTiles();
                round = 0;
                curUnitID = 0;
                break;
            case P1TACTICAL:
                battleStage = BattleStage.P2TACTICAL;
                setAvailableTiles();
                break;
            case P2TACTICAL:
                createUnitsOrder();
                clearTiles();
                if(queueUnits.get(0).getHero()[0] == playerOne) battleStage=BattleStage.P1ROUND;
                else battleStage=BattleStage.P2ROUND;
                round++;
                playerTwo.setSpellDelay(0);
                playerOne.setSpellDelay(0);
                playerOne.setAttackDelay(0);
                playerTwo.setAttackDelay(0);
                playerOne.setUsedUnitThisTurn(false);
                playerTwo.setUsedUnitThisTurn(false);
                if(queueUnits.get(0).getHero()[0].isPlayer()) setUnitAvailableTiles();;
                break;
            case P1ROUND: case P2ROUND:
                playerOne.setUsedUnitThisTurn(false);
                playerTwo.setUsedUnitThisTurn(false);
                removeDeadQueueMembers();
                if(queueUnits.get(0) == null || queueUnits.get(1) == null){
                    createUnitsOrder();
                    decreaseEffectDurations();
                    round++;
                    curUnitID++;
                }else{
                    if(round!=0) {
                        queueUnits.remove(queueUnits.get(0));
                        queueUnits.add(null);
                    }
                }
                if(queueUnits.get(0).getHero()[0] == playerOne) battleStage=BattleStage.P1ROUND;
                else battleStage=BattleStage.P2ROUND;
                if(queueUnits.get(0).getHero()[0].isPlayer()) setUnitAvailableTiles();
                else clearTiles();
                break;
            default:
                break;
        }
    }
    private static void removeDeadQueueMembers(){
        int c = 0;
        for (Iterator<BattleUnit> iterator = queueUnits.iterator(); iterator.hasNext();) {
            BattleUnit reference = iterator.next();
            BattleUnit unit = reference!=null?reference.getHero()[0].getBattleUnits().get(reference.getUnits().get(0).getUnitType()):null;
            if(unit != null && unit.getHealth() <= 0){
                iterator.remove();
                c++;
            }
        }
        for (int i = 0; i < c; i++){
            queueUnits.add(null);
        }
    }
    /**
     * Minden mezőt nem elérhetővé tesz.
     */
    public static void clearTiles(){
        for(int i = 0; i < GameManager.height; i++){
            for( int j = 0; j < GameManager.width; j++){
                battleField.getTiles()[i][j].setAvailable(false);
            }
        }
    }
    /**
     * beállítja az adott körtől függően az elérhető mezőket.
     */
    private static void setAvailableTiles(){
        clearTiles();
        switch (battleStage){
            case P1TACTICAL:
                for(int i = 0; i < height; i++){
                    for(int j = 0; j < width; j++){
                        battleField.getTiles()[i][j].setAvailable(j < startAvailableCols);
                    }
                }
                break;
            case P2TACTICAL:
                for(int i = 0; i < height; i++){
                    for(int j = 0; j < width; j++){
                        battleField.getTiles()[i][j].setAvailable(width-startAvailableCols<=j);
                    }
                }
                break;
            case P1ROUND:
                setUnitAvailableTiles();
                break;
            case P2ROUND:
                setUnitAvailableTiles();
                break;
        }
    }
    public static void setUnitAvailableTiles(){
        clearTiles();
        if(!curPlayer()[0].isUsedUnitThisTurn() && !queueUnits.get(0).isFreezed()){
            if(!isStuck()){
                setReachableTiles();
            }else{
                getBattleField().getTiles()[queueUnits.get(0).getX()][queueUnits.get(0).getY()].setAvailable(true);
            }
        }
    }
    private static void setReachableTiles(){
        BattleUnit cur =  queueUnits.get(0);
        int startx = Math.max(cur.getX()-cur.getSpeed(),0);
        int endx = Math.min(height-1, cur.getX() + cur.getSpeed());
        int starty = Math.max(cur.getY()-cur.getSpeed(),0);
        int endy = Math.min(width-1, cur.getY() + cur.getSpeed());
        for(int i = startx; i<=endx; i++){
            for(int j = starty; j<=endy; j++){
                if(Math.abs(cur.getX()-i)+Math.abs(cur.getY()-j)<=cur.getSpeed()){
                    BattleField.Tile t = battleField.getTiles()[i][j];
                    if(t.getUnitOnTile() == null || (t.getUnitOnTile() != null && (t.getUnitOnTile().getHero()[0] != curPlayer()[0] || t.getUnitOnTile() == cur))){
                        battleField.getTiles()[i][j].setAvailable(true);
                    }
                }
            }
        }
        if(cur.getUnits().get(0).getUnitType() == UnitType.ARCHER){
            startx = Math.max(cur.getX()-1,0);
            endx = Math.min(height-1, cur.getX() + 1);
            starty = Math.max(cur.getY()-1,0);
            endy = Math.min(width-1, cur.getY() + 1);
            boolean found = false;
            for(int i = startx; i<=endx; i++){
                for(int j = starty; j<=endy; j++){
                    if(battleField.getTiles()[i][j].getUnitOnTile() != null && battleField.getTiles()[i][j].getUnitOnTile().getHero()[0] == curEnemy()[0]){
                        found = true;
                        battleField.getTiles()[i][j].setAvailable(false);
                    }
                }
            }
            for(int i = 0; i<height; i++){
                for(int j = 0; j<width; j++){
                    BattleField.Tile t = battleField.getTiles()[i][j];
                    if(t.getUnitOnTile() != null && t.getUnitOnTile().getHero()[0] != curPlayer()[0]){
                        battleField.getTiles()[i][j].setAvailable(!found);
                    }
                }
            }
        }else{
            for(int i = 0; i<height; i++){
                for(int j = 0; j<width; j++){
                    BattleField.Tile t = battleField.getTiles()[i][j];
                    if(t.getUnitOnTile() != null && t.getUnitOnTile().getHero()[0] != curPlayer()[0]){
                        battleField.getTiles()[i][j].setAvailable(
                                Math.abs(curPlayer()[0].getBattleUnits().get(queueUnits.get(0).getUnits().get(0).getUnitType()).getX() - i)<=1
                                        && Math.abs(curPlayer()[0].getBattleUnits().get(queueUnits.get(0).getUnits().get(0).getUnitType()).getY() - j)<=1
                        );
                    }
                }
            }
        }
    }
    /**
     * Megadja, hogy az éppen következő egység be van-e szorulva és ezáltal nem tud lépni.
     * @return be van-e szorulva logikai értékként
     */
    private static boolean isStuck(){
        BattleUnit cur =  queueUnits.get(0);
        int startX = Math.max(0, cur.getX()-1);
        int endX = Math.min(height-1, cur.getX()+1);
        int startY = Math.max(0, cur.getY()-1);
        int endY = Math.min(width-1, cur.getY()+1);
        for(int i = startX; i < endX; i++){
            for(int j = startY; j < endY; j++){
                if(battleField.getTiles()[i][j].getUnitOnTile()==null){
                    return false;
                }
            }
        }
        return true;
    }
    public static Hero[] curPlayer(){
        if(battleStage == BattleStage.P1ROUND) return new Hero[] {playerOne};
        else return new Hero[] {playerTwo};
    }
    public static Hero[] curEnemy(){
        return GameManager.getBattleStage() == BattleStage.P1ROUND ? GameManager.getPlayerTwo() : GameManager.getPlayerOne();
    }
    private static void decreaseEffectDurations(){
        playerOne.decreaseMagicShield();
        playerTwo.decreaseMagicShield();
        playerOne.setSpellDelay(playerOne.getSpellDelay()-1);
        playerTwo.setSpellDelay(playerTwo.getSpellDelay()-1);
        playerOne.setAttackDelay(playerOne.getSpellDelay()-1);
        playerTwo.setAttackDelay(playerTwo.getSpellDelay()-1);
        for(BattleUnit bu: playerOne.getBattleUnits().values()){
            bu.decreaseFrozenEffectDuration();
        }
        for(BattleUnit bu: playerTwo.getBattleUnits().values()){
            bu.decreaseFrozenEffectDuration();
        }
    }
    public static void createUnitsOrder(){
        initializeQueue();
        resetBackAttacks();
        int len = 0;
        for(UnitType type: UnitType.values()){
            if(playerOne.getBattleUnits().containsKey(type) && playerOne.getBattleUnits().get(type).getHealth()>0){
                queueUnits.set(len,playerOne.getBattleUnits().get(type));
                len++;
            }
            if(playerTwo.getBattleUnits().containsKey(type) && playerTwo.getBattleUnits().get(type).getHealth()>0){
                queueUnits.set(len,playerTwo.getBattleUnits().get(type));
                len++;
            }
        }
        for(int iteration = 0; iteration < 10; iteration++){
            for(int i = 0; i < len-1; i++){
                int curEffectiveInitiative = queueUnits.get(i).getInitiative()+queueUnits.get(i).getHero()[0].getMoral();
                int nxtEffectiveInitiative = queueUnits.get(i+1).getInitiative()+queueUnits.get(i+1).getHero()[0].getMoral();
                Random rnd = new Random();
                if(curEffectiveInitiative < nxtEffectiveInitiative){
                    swapQueueUnits(i,i+1);
                }else if( curEffectiveInitiative == nxtEffectiveInitiative && rnd.nextBoolean()){
                    swapQueueUnits(i,i+1);
                }
            }
        }
    }
    /**
     * Megcserél két egységet a sorrendben.
     * @param i1 egyik egység sorszáma
     * @param i2 másik egység sorszáma
     */
    public static void swapQueueUnits(int i1, int i2){
        BattleUnit temp = queueUnits.get(i1);
        queueUnits.set(i1,queueUnits.get(i2));
        queueUnits.set(i2,temp);
    }
}
