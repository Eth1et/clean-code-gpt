package prog1.kotprog.dontstarve.solution;

import prog1.kotprog.dontstarve.solution.character.BaseCharacter;
import prog1.kotprog.dontstarve.solution.character.GameCharacter;
import prog1.kotprog.dontstarve.solution.character.actions.Action;
import prog1.kotprog.dontstarve.solution.character.actions.ActionNone;
import prog1.kotprog.dontstarve.solution.character.actions.ActionInteract;
import prog1.kotprog.dontstarve.solution.character.actions.ActionStep;
import prog1.kotprog.dontstarve.solution.character.actions.ActionStepAndAttack;
import prog1.kotprog.dontstarve.solution.character.actions.ActionAttack;
import prog1.kotprog.dontstarve.solution.character.actions.ActionEat;
import prog1.kotprog.dontstarve.solution.level.BaseField;
import prog1.kotprog.dontstarve.solution.level.Field;
import prog1.kotprog.dontstarve.solution.level.Level;
import prog1.kotprog.dontstarve.solution.level.MapColors;
import prog1.kotprog.dontstarve.solution.level.interactive.InteractiveObjectType;
import prog1.kotprog.dontstarve.solution.utility.Direction;
import prog1.kotprog.dontstarve.solution.utility.Position;

import java.util.*;

/**
 * A játék működéséért felelős osztály.<br>
 * Az osztály a singleton tervezési mintát valósítja meg.
 */
public final class GameManager {
    /**
     * Az osztályból létrehozott egyetlen példány (nem lehet final).
     */
    private static GameManager instance = new GameManager();

    /**
     * Random objektum, amit a játék során használni lehet.
     */
    private final Random random = new Random();

    /**
     * Becsatlakozott-e már emberi játékos.
     */
    private boolean playerJoined;

    /**
     * A játékba becsatlakozott játékosok.
     */
    private Map<String, GameCharacter> characters;

    /**
     * Az összes játékos listája, belépési sorrendben.
     */
    private List<GameCharacter> characterList;

    /**
     * Player character.
     */
    private GameCharacter playerCharacter;

    /**
     * Tutorial módban játszunk-e.
     */
    private boolean tutorial;

    /**
     * Betöltődött-e a pálya.
     */
    private boolean levelLoaded;

    /**
     * Elkezdődött-e a játék.
     */
    private boolean gameStarted;

    /**
     * Vége van-e a játéknak.
     */
    private boolean gameEnded;

    /**
     * Az időpillanat.
     */
    private int currentTime;

    /**
     * A pálya mint mezők 2D-s tömbje.
     */
    private Field[][] map;

    /**
     * Az osztály privát konstruktora.
     */
    private GameManager() {
        initialize();
    }

    /**
     * Inicializálja az adattagokat.
     */
    private void initialize(){
        gameStarted = false;
        levelLoaded = false;
        tutorial = false;
        gameEnded = false;
        playerJoined = false;
        playerCharacter = null;
        currentTime = 0;
        characters = new HashMap<>();
        characterList = new ArrayList<>();
    }

    /**
     * Az osztályból létrehozott példány elérésére szolgáló metódus.
     * @return az osztályból létrehozott példány
     */
    public static GameManager getInstance() {
        return instance;
    }

    /**
     * A létrehozott random objektum elérésére szolgáló metódus.
     * @return a létrehozott random objektum
     */
    public Random getRandom() {
        return random;
    }

    /**
     * Egy karakter becsatlakozása a játékba.<br>
     * A becsatlakozásnak számos feltétele van:
     * <ul>
     *     <li>A pálya már be lett töltve</li>
     *     <li>A játék még nem kezdődött el</li>
     *     <li>Csak egyetlen emberi játékos lehet, a többi karaktert a gép irányítja</li>
     *     <li>A névnek egyedinek kell lennie</li>
     * </ul>
     * @param name a csatlakozni kívánt karakter neve
     * @param player igaz, ha emberi játékosról van szó; hamis egyébként
     * @return a karakter pozíciója a pályán, vagy (Integer.MAX_VALUE, Integer.MAX_VALUE) ha nem sikerült hozzáadni
     */
    public Position joinCharacter(String name, boolean player) {
        if(levelLoaded && !gameStarted && (!playerJoined || !player) && !characters.containsKey(name)){
            Position spawnPosition = getAvailableField();

            if(spawnPosition == null){
                return new Position(Integer.MAX_VALUE, Integer.MAX_VALUE);
            }

            GameCharacter entity = new GameCharacter(name, player, spawnPosition, 100, 100, 1);
            characters.put(name, entity);
            characterList.add(entity);

            if(player){
                playerJoined = true;
                playerCharacter = characters.get(name);
            }

            characters.get(name).getInventory().giveStarterLoot();

            return characters.get(name).getCurrentPosition();
        }
        return new Position(Integer.MAX_VALUE, Integer.MAX_VALUE);
    }

    /**
     * Egy adott nevű karakter lekérésére szolgáló metódus.<br>
     * @param name A lekérdezni kívánt karakter neve
     * @return Az adott nevű karakter objektum, vagy null, ha már a karakter meghalt vagy nem is létezett
     */
    public BaseCharacter getCharacter(String name) {
        return characters.get(name);
    }

    /**
     * Ezen metódus segítségével lekérdezhető, hogy hány karakter van még életben.
     * @return Az életben lévő karakterek száma
     */
    public int remainingCharacters() {
        int c = 0;
        for(GameCharacter character: characterList){
            if(character != null && character.getHp() > 0){
                c++;
            }
        }
        return c;
    }

    /**
     * Ezen metódus segítségével történhet meg a pálya betöltése.<br>
     * A pálya betöltésének azelőtt kell megtörténnie, hogy akár 1 karakter is csatlakozott volna a játékhoz.<br>
     * A pálya egyetlen alkalommal tölthető be, később nem módosítható.
     * @param level a fájlból betöltött pálya
     */
    public void loadLevel(Level level) {
        if(((levelLoaded || gameStarted || !characterList.isEmpty()) && !gameEnded)){
            return;
        }

        initialize();
        map = new Field[level.getWidth()][level.getHeight()];

        for(int x = 0; x < level.getWidth(); x++){
            for(int y = 0; y < level.getHeight(); y++){
                map[x][y] = MapColors.getFieldByColor(level.getColor(x, y));
            }
        }
        levelLoaded = true;
    }

    /**
     * A pálya egy adott pozícióján lévő mező lekérdezésére szolgáló metódus.
     * @param x a vízszintes (x) irányú koordináta
     * @param y a függőleges (y) irányú koordináta
     * @return az adott koordinátán lévő mező
     */
    public BaseField getField(int x, int y) {
        return map[x][y];
    }

    /**
     * Megad egy szabad pontot amely minden másik jétékostól messze van (NAGYON GYORSAN!).
     * @return a számított pont, null ha nincs ilyen
     */
    private Position getAvailableField(){
        for(double dist = 50; dist > 0; dist -= 5){
            for(int x = 0; x < map.length; x++){
                for(int y = 0; y < map[0].length; y++){
                    if(!getField(x, y).isWalkable()) {
                        continue;
                    }

                    Position position = new Position(x, y);
                    boolean correct = true;

                    for(GameCharacter character: characterList){
                        if(character.getCurrentPosition().distanceToPoint(position) < dist){
                            correct = false;
                            break;
                        }
                    }

                    if(correct){
                        return position;
                    }
                }
            }
        }
        return null;
    }

    /**
     * A játék megkezdésére szolgáló metódus.<br>
     * A játék csak akkor kezdhető el, ha legalább 2 karakter már a pályán van,
     * és közülük pontosan az egyik az emberi játékos által irányított karakter.
     * @return igaz, ha sikerült elkezdeni a játékot; hamis egyébként
     */
    public boolean startGame() {
        if(levelLoaded && !gameStarted && remainingCharacters() >= 2 && playerJoined){
            gameStarted = true;
            return true;
        }
        return false;
    }

    /**
     * Kör végi frissítések, karakterek törlése, éhség nő, élettartama csökken az időre menő cuccoknak.
     * Nem megy a magyar nyelv na.
     */
    private void update(){
        for(GameCharacter character: characterList){
            if(character.getHp() != 0){
                character.getHungrier();
                character.getInventory().decreaseTorchDuration();
            }
        }
        for(Field[] row: map){
            for(Field field: row){
                field.decreaseFireTime();
            }
        }

        characters.keySet().removeIf(name -> characters.get(name).getHp() == 0);
        characterList.removeIf(ch -> ch.getHp() == 0);
    }

    /**
     * Végrehajtja a karakterek akcióit.
     * @param playerAction a játékos akciója
     */
    private void handleCharacterActions(Action playerAction){
        for(GameCharacter ch: characterList){
            ch.executeAction(new ActionNone());
        }
        if(playerAction != null){
            playerCharacter.executeAction(playerAction);
        }
        if(!tutorial){
            for (GameCharacter character : characterList) {
                if(playerCharacter.getHp() == 0 || remainingCharacters() <= 1){
                    break;
                }else if (!character.isPlayer()) {
                    character.executeAction(calculateEnemyAction(character));
                }
            }
        }
    }

    /**
     * Ez a metódus jelzi, hogy 1 időegység eltelt.<br>
     * A metódus először lekezeli a felhasználói inputot, majd a gépi ellenfelek cselekvését végzi el,
     * végül eltelik egy időegység.<br>
     * Csak akkor csinál bármit is, ha a játék már elkezdődött, de még nem fejeződött be.
     * @param action az emberi játékos által végrehajtani kívánt akció
     */
    public void tick(Action action) {
        if(!gameStarted || gameEnded){
            return;
        }

        handleCharacterActions(action);

        update();

        if(remainingCharacters() <= 1 || playerCharacter.getHp() == 0){
            gameEnded = true;
            return;
        }

        currentTime++;
    }

    /**
     * Megadja, hogy az adott irányba az adott mezőre tudunk e lépni.
     * @param direction irány
     * @param nextCoordinate koordináta
     * @param nextField mező
     * @return boolean
     */
    private boolean unreachableNextField(Direction direction, Position nextCoordinate, Field nextField){
        return direction == null || GameManager.getInstance().positionOutOfBounds(nextCoordinate) || !nextField.isWalkable();
    }

    /**
     * Megadja, hogy mi a következő lépés ahhoz, hogy eljusson a karakter az adott pontba.
     * @param character a karakter
     * @param target a cél
     * @return az akció
     */
    private Action goTowards(GameCharacter character, Position target){
        float xDif = target.getX() - character.getCurrentPosition().getX();
        float yDif = target.getY() - character.getCurrentPosition().getY();

        Position horizontal = character.getCurrentPosition().added(new Position(Math.signum(xDif)*character.getSpeed(), 0));
        Field horizontalField = getFieldByPosition(horizontal.getNearestWholePosition());

        Position vertical = character.getCurrentPosition().added(new Position(0, Math.signum(yDif)*character.getSpeed()));
        Field verticalField = getFieldByPosition(vertical.getNearestWholePosition());

        Direction direction = null;
        Position nextCoordinate = null;
        Position nextPosition = null;
        Field nextField = null;

        if(Math.abs(xDif) > Math.abs(yDif) && horizontalField != null && horizontalField.isWalkable()){
            direction = xDif >= 0?Direction.RIGHT:Direction.LEFT;
            nextCoordinate = horizontal.getNearestWholePosition();
            nextPosition = horizontal;
            nextField = horizontalField;
        }else if (verticalField != null && verticalField.isWalkable()){
            direction = yDif >= 0?Direction.DOWN:Direction.UP;
            nextCoordinate = vertical.getNearestWholePosition();
            nextPosition = vertical;
            nextField = verticalField;
        }

        return nextStep(character, target, direction, nextCoordinate, nextPosition, nextField);
    }

    /**
     * Megadja, hogy mi a következő lépés, ahhoz hogy odaérjünk.
     * @param character karakter
     * @param target célpont
     * @param direction irány
     * @param nextCoordinate kövi koordináta
     * @param nextPosition kövi pontos pozi
     * @param nextField kövi mező
     * @return az akció
     */
    private Action nextStep(GameCharacter character, Position target, Direction direction, Position nextCoordinate, Position nextPosition, Field nextField){
        if(unreachableNextField(direction, nextCoordinate, nextField)){
            return character.getCurrentPosition().distanceToPoint(target) <= 2 ? new ActionAttack() : new ActionNone();
        }else{
            return nextPosition.distanceToPoint(target) <= 2 ? new ActionStepAndAttack(direction) : new ActionStep(direction);
        }
    }

    /**
     * Kiszámolja a gépi ellenfelek következő lépését.
     * @param character az adott ellenfél
     * @return a végrehajtandó lépés ( akció )
     */
    private Action calculateEnemyAction(GameCharacter character){
        if(character.getHunger() > 35 || (playerCharacter.getHp() < 20 && character.getHp() >= 20)){
            return goTowards(character, playerCharacter.getCurrentPosition());
        }else if (character.getInventory().hasFood() != -1){
            return new ActionEat(character.getInventory().hasFood());
        }else{
            return goForFood(character);
        }
    }

    /**
     * A karakter bogyót/répát szed, ha nincs olyan mezőn akkor pedig odamegy.
     * @param character a karakter
     * @return az akció
     */
    private Action goForFood(GameCharacter character){
        Position position = character.getCurrentPosition();
        Field currentField = getFieldByPosition(position.getNearestWholePosition());

        if(currentField != null && (currentField.hasBerry() || currentField.hasCarrot())){
            return new ActionInteract();
        }else{
            Position nearestBerry = nearestObject(character, InteractiveObjectType.BERRY);
            Position nearestCarrot = nearestObject(character, InteractiveObjectType.CARROT);

            if(nearestCarrot != null && nearestBerry != null){
                Position target = position.distanceToPoint(nearestBerry) <= position.distanceToPoint(nearestCarrot)?nearestBerry:nearestCarrot;
                return goTowards(character, target);
            }else if(nearestCarrot != null){
                return goTowards(character, nearestCarrot);
            }else if(nearestBerry != null){
                return goTowards(character, nearestBerry);
            }else{
                return goTowards(character, playerCharacter.getCurrentPosition());
            }
        }
    }

    /**
     * Megadja a legközelebbi objektum pozícióját.
     * @param character A karakterhez viszonyítva
     * @param type a keresett objektum típusa
     * @return pos
     */
    private Position nearestObject(GameCharacter character, InteractiveObjectType type){
        float min = Float.MAX_VALUE;
        Position res = null;
        for(int i = 0; i < map.length; i++){
            for(int j = 0; j < map[0].length; j++){
                float dist = character.getCurrentPosition().distanceToPoint(new Position(i, j));
                if(map[i][j].getInteractiveObject() != null &&
                        map[i][j].getInteractiveObject().getType() == type && dist < min){
                    res = new Position(i, j);
                    min = dist;
                }
            }
        }
        return res;
    }

    /**
     * Megadja az adott pozícióhoz tartozó koordinátát.
     * @param position a pozíció
     * @return a hozzá tartozó mező
     */
    public Field getFieldByPosition(Position position){
        if(positionOutOfBounds(position)){
            return null;
        }

        Position wholePosition = position.getNearestWholePosition();

        wholePosition.setX(Math.max(0, Math.min(map.length-1, wholePosition.getX())));
        wholePosition.setY(Math.max(0, Math.min(map[0].length-1, wholePosition.getY())));

        return map[(int)wholePosition.getX()][(int)wholePosition.getY()];
    }

    /**
     * Megadja hogy position a pályán belülre esik-e.
     * @param position pozíció
     * @return belülre esik-e
     */
    private boolean positionOutOfBounds(Position position){
        return -0.5 > position.getX() || position.getX() > map.length - 0.5 || -0.5 > position.getY() || position.getY() > map[0].length - 0.5;
    }

    /**
     * @param reference A karakterhez
     * @return A karakterhez legközelebbi karakter
     */
    public GameCharacter getNearestCharacter(GameCharacter reference, int threshold){
        GameCharacter min = null;
        for(GameCharacter character: characterList){
            float curDist = reference.getCurrentPosition().distanceToPoint(character.getCurrentPosition());
            float minDist = min == null? Float.MAX_VALUE : reference.getCurrentPosition().distanceToPoint(min.getCurrentPosition());

            if(character.getHp() > 0 && !character.getName().equals(reference.getName()) && curDist <= threshold && curDist < minDist){
                min = character;
            }
        }
        return min;
    }

    /**
     * Ezen metódus segítségével lekérdezhető az aktuális időpillanat.<br>
     * A játék kezdetekor ez az érték 0 (tehát a legelső időpillanatban az idő 0),
     * majd minden eltelt időpillanat után 1-gyel növelődik.
     * @return az aktuális időpillanat
     */
    public int time() {
        return this.currentTime;
    }

    /**
     * Ezen metódus segítségével lekérdezhetjük a játék győztesét.<br>
     * Amennyiben a játéknak még nincs vége (vagy esetleg nincs győztes), akkor null-t ad vissza.
     * @return a győztes karakter vagy null
     */
    public BaseCharacter getWinner() {
        if(!gameEnded){
            return null;
        }
        for(GameCharacter character: characterList){
            if(character.getHp() > 0){
                return character;
            }
        }
        return null;
    }

    /**
     * Ezen metódus segítségével lekérdezhetjük, hogy a játék elkezdődött-e már.
     * @return igaz, ha a játék már elkezdődött; hamis egyébként
     */
    public boolean isGameStarted() {
        return this.gameStarted;
    }

    /**
     * Ezen metódus segítségével lekérdezhetjük, hogy a játék befejeződött-e már.
     * @return igaz, ha a játék már befejeződött; hamis egyébként
     */
    public boolean isGameEnded() {
        return this.gameEnded;
    }

    /**
     * Ezen metódus segítségével beállítható, hogy a játékot tutorial módban szeretnénk-e elindítani.<br>
     * Alapértelmezetten (ha nem mondunk semmit) nem tutorial módban indul el a játék.<br>
     * Tutorial módban a gépi karakterek nem végeznek cselekvést, csak egy helyben állnak.<br>
     * A tutorial mód beállítása még a karakterek csatlakozása előtt történik.
     * @param tutorial igaz, amennyiben tutorial módot szeretnénk; hamis egyébként
     */
    public void setTutorial(boolean tutorial) {
        this.tutorial = tutorial;
    }
}
