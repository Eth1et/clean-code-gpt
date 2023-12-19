package Heroes.Controllers;

import Heroes.*;
import Heroes.Enums.BattleStage;
import Heroes.Enums.SpellType;
import Heroes.Enums.UnitType;
import Heroes.Spells.Spell;
import Heroes.Units.BattleUnit;
import Heroes.Units.Unit;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.geometry.Point3D;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.scene.text.TextAlignment;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.URL;
import java.util.*;

/**
 * A csata jelenet felhasználói felületéért, bizonyos csata funkciók működéséért felelőpős osztály.
 */
public class BattleController implements Initializable {

    private Stage stage;
    private Scene scene;
    private Parent root;

    private Slot[] inventorySlots;
    private boolean firstPlayer;

    public void setFirstPlayer(boolean firstPlayer) {
        this.firstPlayer = firstPlayer;
    }

    @FXML
    private Label labelBlueName, labelRedName,labelRedMana,labelBlueMana,labelInventoryTitle1,labelInventoryTitle2,labelInventoryTitle3,labelInventoryTitle4,labelInventoryTitle5,labelInventoryTitle6;
    @FXML
    private Label labelInventoryCounter1,labelInventoryCounter2,labelInventoryCounter3,labelInventoryCounter4,labelInventoryCounter5,labelInventoryCounter6, labelRoundCounter;
    @FXML
    private ImageView imgvBlue,imgvRed,imgvManaIcon1,imgvManaIcon2,imgvInventory1,imgvInventory2,imgvInventory3,imgvInventory4,imgvInventory5,imgvInventory6;
    @FXML
    private VBox vboxGodParent,logParent;
    @FXML
    private GridPane gridpBattlefield,gridpInventoryParent,gridpQueue;
    @FXML
    private Button btnBackToMainMenu,btnEndTurn;

    @FXML
    private void backToMainMenu(ActionEvent event) throws IOException {
        root = FXMLLoader.load(Objects.requireNonNull(App.class.getResource("Scenes/MainMenu.fxml")));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root);
        stage.setScene(scene);
        stage.sizeToScene();
        stage.centerOnScreen();
        stage.show();
    }
    @FXML
    private void endTurn(ActionEvent e){
        switch (GameManager.getBattleStage()){
            case P1TACTICAL:
                GameManager.nextBattleStage();
                firstPlayer = false;
                logTacticalStageHelp();
                setUpInventoryButtons();
                showUnitsInInventory();
                updateTilesVisuals();
                if(!GameManager.isIsPVP()){
                    deployAiUnits();
                }else{
                    btnEndTurn.setDisable(true);
                }
                break;
            case P2TACTICAL: case P1ROUND: case P2ROUND:
                GameManager.nextBattleStage();
                updateUnitsQueue();
                if(!GameManager.isIsPVP() && GameManager.getBattleStage()==BattleStage.P2ROUND){
                    aiTurn();
                }
                setUpInventoryButtons();
                updateTilesVisuals();
                updateUnitsQueue();
                setUpPlayerTurn();
            case GAMEOVER:
                break;
        }
        updateRoundLabel();
        updateMana();
    }
    private int[] getMostTargetHits(){
        int area = Spell.getSpellArea(SpellType.FIREBALL);
        int[] idealSpot = {0,0};
        int enemyHits = 0, friendlyHits = 0;
        for(BattleField.Tile[] row: GameManager.getBattleField().getTiles()) {
            for (BattleField.Tile tile : row) {
                int startY = Math.max(tile.getX() - area, 0);
                int endY = Math.min(tile.getX() + area, GameManager.height - 1);
                int startX = Math.max(tile.getY() - area, 0);
                int endX = Math.min(tile.getY() + area, GameManager.width - 1);
                //GO THROUGH SURROUNDING TILES TILES
                int fh = 0, eh = 0;
                for(int i = startY; i <= endY ; i++){
                    for(int j = startX; j <= endX; j++){
                        if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!=null  && GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] == curHero()[0]){
                            fh++;
                        }else if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!=null){
                            eh++;
                        }
                    }
                }
                //IF NUMBER OF HITS IS GREATER OR EQUAL BUT LESS FRIENDLY UNITS IN AREA -> SET IDEAL
                if(eh > enemyHits || eh == enemyHits && fh < friendlyHits){
                    idealSpot = new int[] {tile.getX(), tile.getY()};
                    enemyHits = eh;
                    friendlyHits = fh;
                }
            }
        }
        return new int[] {idealSpot[0], idealSpot[1], enemyHits};
    }
    private void aiTurn(){
        int emptyLines = 3;
        Text headerColored = new Text(" PIROS "+GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
        headerColored.setFill(new Color(1,0,0,1));
        addBattleLog(new Text("==================="),headerColored,new Text(" köre "),new Text("==================="));
        int tX = -1, tY = -1;
        if(!GameManager.curEnemy()[0].isMagicShielded() && curHero()[0].getSpellDelay() <= 0){
            int[] ret = getMostTargetHits();
            if(curHero()[0].getSpells().containsKey(SpellType.RESURRECT) && curHero()[0].hasUnitWithLowHealth() && curHero()[0].getMana() >= Spell.getSpellManaCost(SpellType.RESURRECT)){
                tX = curHero()[0].getBattleUnits().get(curHero()[0].getUnitWithLowHealth()).getX();
                tY = curHero()[0].getBattleUnits().get(curHero()[0].getUnitWithLowHealth()).getY();

                logSpellOutcome(SpellType.RESURRECT, GameManager.castSpell(SpellType.RESURRECT,tX, tY), tX, tY);
                emptyLines--;
            }
            else if(ret[2] == 0){return;}
            else if(curHero()[0].getSpells().containsKey(SpellType.LIGHTNINGSTRIKE) && ret[2] == 1 && curHero()[0].getMana() >= Spell.getSpellManaCost(SpellType.LIGHTNINGSTRIKE)){
                UnitType target;
                if(GameManager.curEnemy()[0].hasUnitWithLowHealth()){
                   target = GameManager.curEnemy()[0].getUnitWithLowHealth();
                }else{
                    target = GameManager.curEnemy()[0].getStrongestUnit();
                }
                tX = GameManager.curEnemy()[0].getBattleUnits().get(target).getX();
                tY = GameManager.curEnemy()[0].getBattleUnits().get(target).getY();
                logSpellOutcome(SpellType.LIGHTNINGSTRIKE, GameManager.castSpell(SpellType.LIGHTNINGSTRIKE, tX, tY), tX, tY);
                emptyLines--;
            }
            else if(curHero()[0].getSpells().containsKey(SpellType.FIREBALL) && curHero()[0].getMana() >= Spell.getSpellManaCost(SpellType.FIREBALL)){
                logSpellOutcome(SpellType.FIREBALL,GameManager.castSpell(SpellType.FIREBALL,ret[0],ret[1]),ret[0],ret[1]);
                emptyLines--;
            }
            else{
                Random rnd = new Random();
                if(curHero()[0].getSpells().containsKey(SpellType.FREEZE) && rnd.nextBoolean() && curHero()[0].getMana() >= Spell.getSpellManaCost(SpellType.FREEZE)){
                    UnitType target = GameManager.curEnemy()[0].getStrongestUnit();
                    tX  = GameManager.curEnemy()[0].getBattleUnits().get(target).getX();
                    tY  = GameManager.curEnemy()[0].getBattleUnits().get(target).getX();
                    logSpellOutcome(SpellType.FREEZE, GameManager.castSpell(SpellType.FREEZE,tX ,tY ), tX, tY);
                    emptyLines--;
                }
                else if(curHero()[0].getSpells().containsKey(SpellType.MAGICSHIELD) && curHero()[0].getMana() >= Spell.getSpellManaCost(SpellType.MAGICSHIELD)){
                    logSpellOutcome(SpellType.MAGICSHIELD,GameManager.castSpell(SpellType.MAGICSHIELD, 0, 0),0,0);
                    emptyLines--;
                }
            }
            if(tX!=-1&&tY!=-1){
                if(GameManager.getBattleField().getTiles()[tX][tY].getUnitOnTile().getHero()[0].getBattleUnits().get(GameManager.getBattleField().getTiles()[tX][tY].getUnitOnTile().getUnits().get(0).getUnitType()).getHealth() <= 0){
                    GameManager.getBattleField().getTiles()[tX][tY].removeUnitFromTile();
                }
            }
            updateTilesVisuals();
            setUpBattlefieldTiles();
            updateBattleFieldGrid();
            handleGameOver(GameManager.checkForGameOver());
            if(GameManager.getBattleStage()==BattleStage.GAMEOVER) return;
        }
        else if(curHero()[0].getAttackDelay() <= 0){
            tX=-1;
            tY=-1;
            UnitType target = null;
            if(GameManager.curEnemy()[0].hasUnitWithLowHealth()){
                target = GameManager.curEnemy()[0].getUnitWithLowHealth();
            }else{
                target = GameManager.curEnemy()[0].getStrongestUnit();
            }
            if(target != null) {
                tX=GameManager.curEnemy()[0].getBattleUnits().get(target).getX();
                tY=GameManager.curEnemy()[0].getBattleUnits().get(target).getY();
                logHeroAttackOutcome(GameManager.heroAttack(tX,tY),tX,tY);
                emptyLines--;
            }
            if(tX!=-1&&tY!=-1){
                if(GameManager.getBattleField().getTiles()[tX][tY].getUnitOnTile().getHero()[0].getBattleUnits().get(GameManager.getBattleField().getTiles()[tX][tY].getUnitOnTile().getUnits().get(0).getUnitType()).getHealth() <= 0){
                    GameManager.getBattleField().getTiles()[tX][tY].removeUnitFromTile();
                }
            }
            updateTilesVisuals();
            setUpBattlefieldTiles();
            updateBattleFieldGrid();
            handleGameOver(GameManager.checkForGameOver());
            if(GameManager.getBattleStage()==BattleStage.GAMEOVER) return;
        }
        if(!GameManager.getQueueUnits().get(0).isFreezed() && !curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).isFreezed()){
            BattleUnit cur =  GameManager.getQueueUnits().get(0);
            tX = -1;
            tY = -1;
            int startX = Math.max(0, cur.getX()-1);
            int endX = Math.min(GameManager.height-1, cur.getX()+1);
            int startY = Math.max(0, cur.getY()-1);
            int endY = Math.min(GameManager.width-1, cur.getY()+1);
            boolean hasEnemyInNeighbour = false;
            UnitType enemy = null;
            for(int i = startX; i < endX; i++){
                for(int j = startY; j < endY; j++){
                    if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!=null &&
                            GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] == GameManager.curEnemy()[0]){
                        hasEnemyInNeighbour=true;
                        enemy = GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getUnits().get(0).getUnitType();
                        break;
                    }
                }
            }
            if(hasEnemyInNeighbour){
                if(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType() == UnitType.ARCHER){
                    int maxDist = 0;
                    int startx = Math.max(cur.getX()-cur.getSpeed(),0);
                    int endx = Math.min(GameManager.height-1, cur.getX() + cur.getSpeed());
                    int starty = Math.max(cur.getY()-cur.getSpeed(),0);
                    int endy = Math.min(GameManager.width-1, cur.getY() + cur.getSpeed());
                    for(int i = startx; i<=endx; i++){
                        for(int j = starty; j<=endy; j++){
                            int dist = Math.abs(cur.getX()-i)+Math.abs(cur.getY()-j);
                            if(dist<=cur.getSpeed()){
                                if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() == null && dist > maxDist){
                                    maxDist = dist;
                                    tX = i;
                                    tY = j;
                                }
                            }
                        }
                    }
                    int binX = tX, binY = tY;
                    GameManager.getBattleField().swapTiles(cur.getX(),cur.getY(),binX,binY);
                    GameManager.getQueueUnits().get(0).setX(tX);
                    GameManager.getQueueUnits().get(0).setY(tY);
                    curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setX(tX);
                    curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setY(tY);
                    setUpBattlefieldTiles();
                    updateBattleFieldGrid();
                    updateTilesVisuals();
                    logUnitMoved(tX,tY);
                    emptyLines--;
                }
                else{
                    tX = GameManager.curEnemy()[0].getBattleUnits().get(enemy).getX();
                    tY = GameManager.curEnemy()[0].getBattleUnits().get(enemy).getY();
                    logUnitAttack(GameManager.unitAttackUnit(tX,tY),tX,tY);
                    emptyLines--;
                }
            }
            else{
                if(cur.getUnits().get(0).getUnitType()==UnitType.ARCHER){
                    if(GameManager.curEnemy()[0].hasUnitWithLowHealth()){
                        tX = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getUnitWithLowHealth()).getX();
                        tY = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getUnitWithLowHealth()).getY();
                    }else{
                        tX = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getStrongestUnit()).getX();
                        tY = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getStrongestUnit()).getY();
                    }
                    logUnitAttack(GameManager.unitAttackUnit(tX,tY),tX,tY);
                    if(curHero()[0].getBattleUnits().get(cur.getUnits().get(0).getUnitType()).getHealth() <= 0){
                        GameManager.getBattleField().getTiles()[curHero()[0].getBattleUnits().get(cur.getUnits().get(0).getUnitType()).getX()][curHero()[0].getBattleUnits().get(cur.getUnits().get(0).getUnitType()).getY()].removeUnitFromTile();
                    }
                    if(GameManager.getBattleField().getTiles()[tX][tY].getUnitOnTile().getHealth() <= 0){
                        GameManager.getBattleField().getTiles()[tX][tY].removeUnitFromTile();
                    }
                    setUpBattlefieldTiles();
                    updateBattleFieldGrid();
                    updateTilesVisuals();
                    emptyLines--;
                }
                else{
                    int minDist = 3600;
                    int startx = Math.max(cur.getX()-cur.getSpeed(),0);
                    int endx = Math.min(GameManager.height-1, cur.getX() + cur.getSpeed());
                    int starty = Math.max(cur.getY()-cur.getSpeed(),0);
                    int endy = Math.min(GameManager.width-1, cur.getY() + cur.getSpeed());
                    for(int i = startx; i<=endx; i++){
                        for(int j = starty; j<=endy; j++){
                            int dist = Math.abs(cur.getX()-i)+Math.abs(cur.getY()-j);
                            if(dist<=cur.getSpeed() && dist <= minDist && GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() != null
                                    && GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] == GameManager.curEnemy()[0]){
                                tX = i;
                                tY = j;
                                minDist = dist;
                            }
                        }
                    }
                    if(minDist != 3600){
                        List<int[]> points = getFreePointsAroundUnit(tX,tY);
                        int minEnemies = 22222;
                        int targetX = -1,targetY = -1;
                        for(int[] point : points){
                            int enemyCount = 0;
                            startx = Math.max(point[0]-1,0);
                            endx = Math.min(GameManager.height-1, point[0] + 1);
                            starty = Math.max(point[1]-1,0);
                            endy = Math.min(GameManager.width-1, point[1] + 1);
                            for(int i = startx; i<=endx; i++){
                                for(int j = starty; j<=endy; j++){
                                    if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() != null &&
                                            GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] == GameManager.curEnemy()[0]){
                                        enemyCount++;
                                    }
                                }
                            }
                            if(minEnemies > enemyCount){
                                targetX = point[0];
                                targetY = point[1];
                            }
                        }
                        tX = targetX;
                        tY = targetY;
                        GameManager.getBattleField().swapTiles(cur.getX(),cur.getY(),tX,tY);
                        GameManager.getQueueUnits().get(0).setX(tX);
                        GameManager.getQueueUnits().get(0).setY(tY);
                        curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setX(tX);
                        curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setY(tY);
                        setUpBattlefieldTiles();
                        updateBattleFieldGrid();
                        updateTilesVisuals();
                        logUnitMoved(tX,tY);
                        emptyLines--;
                    }
                    else{
                        if(GameManager.curEnemy()[0].hasUnitWithLowHealth()){
                            tX = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getUnitWithLowHealth()).getX();
                            tY = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getUnitWithLowHealth()).getY();
                        }else{
                            tX = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getStrongestUnit()).getX();
                            tY = GameManager.curEnemy()[0].getBattleUnits().get(GameManager.curEnemy()[0].getStrongestUnit()).getY();
                        }
                        System.out.println(cur.getX()+","+cur.getY());
                        minDist = 3666;
                        startx = Math.max(cur.getX()-cur.getSpeed(),0);
                        endx = Math.min(GameManager.height-1, cur.getX() + cur.getSpeed());
                        starty = Math.max(cur.getY()-cur.getSpeed(),0);
                        endy = Math.min(GameManager.width-1, cur.getY() + cur.getSpeed());
                        int targetX = -1, targetY = -1;
                        for(int i = startx; i<=endx; i++){
                            for(int j = starty; j<=endy; j++){
                                int dist = Math.abs(tX-i)+Math.abs(tY-j);
                                if(Math.abs(cur.getX()-i)+Math.abs(cur.getY()-j)<=cur.getSpeed() && dist < minDist && GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() == null){
                                    targetX = i;
                                    targetY = j;
                                    minDist = dist;
                                }
                            }
                        }
                        tX=targetX;
                        tY=targetY;
                        GameManager.getBattleField().swapTiles(tX,tY,cur.getX(),cur.getY());
                        GameManager.getQueueUnits().get(0).setX(tX);
                        GameManager.getQueueUnits().get(0).setY(tY);
                        curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setX(tX);
                        curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setY(tY);
                        setUpBattlefieldTiles();
                        updateBattleFieldGrid();
                        updateTilesVisuals();
                        logUnitMoved(tX,tY);
                        emptyLines--;
                    }
                }
                setUpBattlefieldTiles();
                updateBattleFieldGrid();
                handleGameOver(GameManager.checkForGameOver());
            }
        }
        setUpBattlefieldTiles();
        updateBattleFieldGrid();
        updateTilesVisuals();
        for(int i = 0; i < emptyLines; i++){
            addBattleLog();
        }
    }
    private List<int[]> getFreePointsAroundUnit(int x, int y){
        List<int[]> ret = new ArrayList<>();

        int startx = Math.max(x-1,0);
        int endx = Math.min(GameManager.height-1, x + 1);
        int starty = Math.max(y-1,0);
        int endy = Math.min(GameManager.width-1, y + 1);
        for(int i = startx; i<=endx; i++){
            for(int j = starty; j<=endy; j++){
                if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() == null){
                    ret.add(new int[] {i,j});
                }
            }
        }

        return ret;
    }
    private void setUpPlayerTurn(){
        setUpSpellButtons();
        logPlayerTurn();
        unselectInventoryButtons();
        setUpUnitBattleTiles();
        setUpHeroButtons();
    }
    private void updateMana(){
        labelBlueMana.setText(String.valueOf(GameManager.getPlayerOne()[0].getMana()));
        labelRedMana.setText(String.valueOf(GameManager.getPlayerTwo()[0].getMana()));
    }

    private void updateRoundLabel(){
        labelRoundCounter.setText(GameManager.getRound()+". Kör");
    }
    private void updateUnitsQueue(){
        int i = 0;
        for(BattleUnit battleUnit: GameManager.getQueueUnits()){
            if(battleUnit != null && battleUnit.getHealth() > 0){
                ((ImageView)(((Pane)(gridpQueue.getChildren().get(i))).getChildren().get(0))).setImage(new Image(App.class.getResource("Images/"+battleUnit.getUnits().get(0).getUnitType().toString().toLowerCase()+".png").toString()));
                (((Pane)(gridpQueue.getChildren().get(i))).getChildren().get(0)).rotationAxisProperty().set(new Point3D(0,1,0));
                (((Pane)(gridpQueue.getChildren().get(i))).getChildren().get(0)).rotateProperty().set(180);
                if(battleUnit.getHero()[0] == GameManager.getPlayerOne()[0]){
                    gridpQueue.getChildren().get(i).getStyleClass().removeAll("empty","redUnit");
                    gridpQueue.getChildren().get(i).getStyleClass().add("blueUnit");
                }else{
                    gridpQueue.getChildren().get(i).getStyleClass().removeAll("blueUnit","empty");
                    gridpQueue.getChildren().get(i).getStyleClass().add("redUnit");
                }
            }else{
                ((ImageView)(((Pane)(gridpQueue.getChildren().get(i))).getChildren().get(0))).setImage(null);

                gridpQueue.getChildren().get(i).getStyleClass().removeAll("blueUnit","redUnit");
                gridpQueue.getChildren().get(i).getStyleClass().add("empty");
            }
            i++;
        }
    }
    private void deployAiUnits(){
        Random rnd = new Random();
        int previousY = 1 + rnd.nextInt(GameManager.height-2);
        for(List<Unit>  unit:GameManager.getPlayerTwo()[0].getUnits().values()){
            if(unit.size()>0){
                int[] pos = new int[2];
                int area = 1+rnd.nextInt(3);
                if(unit.get(0).getUnitType()==UnitType.ARCHER){
                    pos[1] = getEmptyTileY(11,area,previousY);
                    pos[0] = 11;
                }
                else{
                    System.arraycopy(getEmptyTile(area,previousY),0,pos,0,2);
                }

                deployAiUnit(pos[1],pos[0],unit.get(0).getUnitType());
            }
        }
    }
    private int[] getEmptyTile( int area, int originIndex){
        Random rnd = new Random();
        int y = Math.min(GameManager.height-1, Math.max(0, originIndex + rnd.nextInt(area*2+1)-area));
        int x = 10 + rnd.nextInt(2);
        if(GameManager.getBattleField().getTiles()[y][x].getUnitOnTile()==null) return new int[]{x,y};
        else return getEmptyTile(area,originIndex);
    }
    private int getEmptyTileY(int x, int area, int originIndex){
        Random rnd = new Random();
        int y = Math.min(GameManager.height-1, Math.max(0, originIndex + rnd.nextInt(area*2+1)-area ));
        if(GameManager.getBattleField().getTiles()[y][x].getUnitOnTile()==null) return y;
        else return getEmptyTileY(x, area,originIndex);
    }
    private void updateTilesVisuals(){
        for(int i = 0; i < GameManager.height; i++){
            for( int j = 0; j < GameManager.width; j++){
                gridpBattlefield.getChildren().get(i*GameManager.width+j).getStyleClass().clear();
                BattleField.Tile cur = GameManager.getBattleField().getTiles()[i][j];
                if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!=null){
                    GameManager.getBattleField().getTiles()[i][j].updateLabel();
                }
                switch (cur.getTileState()){
                    case RED:
                        if(cur.isAvailable()){
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("redTileAvailable");
                        }else{
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("redTile");
                        }
                        break;
                    case BLUE:
                        if(cur.isAvailable()){
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("blueTileAvailable");
                        }else{
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("blueTile");
                        }
                        break;
                    case NEUTRAL:
                        if(cur.isAvailable()){
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("neutralTileAvailable");
                        }else{
                            cur.getPane().getStyleClass().removeAll();
                            cur.getPane().getStyleClass().add("neutralTile");
                        }
                        break;
                }
                if(cur.isSelected()){
                    cur.getPane().getStyleClass().add("selectedTile");
                }else{
                    cur.getPane().getStyleClass().removeAll("selectedTile");
                }
                if(cur.isSpellTarget()){
                    cur.getPane().getStyleClass().add("spellTargetTile");
                }else{
                    cur.getPane().getStyleClass().removeAll("spellTargetTile");
                }
            }
        }
    }
    private void addBattleLog(Text... texts){
        if(logParent.getChildren().size()==4) logParent.getChildren().remove(0);

        for(Text text : texts){
            if(text.getFill() == Color.BLACK){
                text.setFill(Color.WHITE);
            }
            text.setFont(Font.font("SansSerif",15));
        }

        TextFlow tf = new TextFlow(texts);
        tf.setTextAlignment(TextAlignment.CENTER);
        tf.getStyleClass().add("eventLog");
        logParent.getChildren().add(tf);
    }
    public void selectTile(int i, int j){
        switch (GameManager.getBattleStage()){
            case P1TACTICAL: case P2TACTICAL:
                if(curHero()[0].isPlayer()) {
                    BattleField.Tile prevSelected = GameManager.getSelectedTile();
                    GameManager.setSelectedTile(GameManager.getBattleField().getTiles()[i][j]);
                    if(GameManager.getSelectedUnitType() != null){
                        deployUnit(i,j);
                    }else if(prevSelected!= null && prevSelected != GameManager.getSelectedTile() && prevSelected.isAvailable() && GameManager.getSelectedTile().isAvailable()
                            && (prevSelected.getUnitOnTile()!=null || GameManager.getSelectedTile().getUnitOnTile()!=null)){
                        GameManager.getBattleField().swapTiles(prevSelected.getX(),prevSelected.getY(),GameManager.getSelectedTile().getX(),GameManager.getSelectedTile().getY());
                        if(prevSelected.getUnitOnTile()!=null){
                            curHero()[0].getBattleUnits().get(prevSelected.getUnitOnTile().getUnits().get(0).getUnitType()).setX(prevSelected.getX());
                            curHero()[0].getBattleUnits().get(prevSelected.getUnitOnTile().getUnits().get(0).getUnitType()).setY(prevSelected.getY());
                        }
                        if(GameManager.getSelectedTile().getUnitOnTile()!=null){
                            curHero()[0].getBattleUnits().get(GameManager.getSelectedTile().getUnitOnTile().getUnits().get(0).getUnitType()).setX(GameManager.getSelectedTile().getX());
                            curHero()[0].getBattleUnits().get(GameManager.getSelectedTile().getUnitOnTile().getUnits().get(0).getUnitType()).setY(GameManager.getSelectedTile().getY());
                        }
                        prevSelected.disselectTile();
                        GameManager.getSelectedTile().disselectTile();
                        GameManager.setSelectedTile(null);
                        setUpBattlefieldTiles();
                        updateBattleFieldGrid();
                    }
                }
        }
    }
    private void deployAiUnit(int i, int j, UnitType unitType){
        BattleField.Tile[][] tiles = GameManager.getBattleField().getTiles();
        if(tiles[i][j].getUnitOnTile()==null && tiles[i][j].isAvailable()){
            tiles[i][j].addUnitToTile(curHero()[0].getBattleUnits().get(unitType), true);
            tiles[i][j].getUnitOnTile().setX(j);
            tiles[i][j].getUnitOnTile().setY(i);
            colorTile(tiles[i][j]);
        }
    }
    private void deployUnit(int i, int j){
        if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()==null && GameManager.getBattleField().getTiles()[i][j].isAvailable()){
            GameManager.getBattleField().getTiles()[i][j].disselectTile();
            Pane invSlotPane = (Pane)gridpInventoryParent.getChildren().get(GameManager.getSelectedUnitType().getValue());
            invSlotPane.disableProperty().set(true);
            invSlotPane.getStyleClass().removeAll("selectedInventorySlot");
            GameManager.getBattleField().getTiles()[i][j].addUnitToTile(curHero()[0].getBattleUnits().get(GameManager.getSelectedUnitType()),!firstPlayer);
            colorTile(GameManager.getBattleField().getTiles()[i][j]);
            GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().setX(i);
            GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().setY(j);
            GameManager.setSelectedTile(null);
            GameManager.setSelectedUnitType(null);
            boolean hasUnplacedUnits = false;
            for(Node node: gridpInventoryParent.getChildren()){
                if(!node.disableProperty().get()){
                    hasUnplacedUnits=true;
                    break;
                }
            }
            if(!hasUnplacedUnits) btnEndTurn.setDisable(false);
        }
    }
    private void handleGameOver(int code){
        switch (code){
            case 0:
                return;
            case 1:
                unsetTilesAfterHeroMove();
                btnEndTurn.setDisable(true);
                if(GameManager.isIsPVP()){
                    Text t1 = new Text("Győzött a ");
                    Text t2 = new Text("KÉK játékos");
                    t2.setFill(Color.ROYALBLUE);
                    Text t3 = new Text("!!!");
                    addBattleLog(t1,t2,t3);
                }else{
                    addBattleLog(new Text("Győztél!!!"));
                }
                break;
            case 2:
                unsetTilesAfterHeroMove();
                btnEndTurn.setDisable(true);
                if(GameManager.isIsPVP()){
                    Text t1 = new Text("Győzött a ");
                    Text t2 = new Text("PIROS játékos");
                    t2.setFill(Color.RED);
                    Text t3 = new Text("!!!");
                    addBattleLog(t1,t2,t3);
                }else{
                    addBattleLog(new Text("Vesztettél!!!"));
                }
                break;
            case 3:
                unsetTilesAfterHeroMove();
                btnEndTurn.setDisable(true);
                addBattleLog( new Text("Döntetlen lett a meccs kimenetele!!!"));
                break;
        }
    }
    private void colorTile(BattleField.Tile tile){
        if(tile.getUnitOnTile()!=null){
            if(firstPlayer) tile.setTileBlue();
            else tile.setTileRed();
        }else{
            tile.setTileNeutral();
        }
    }
    private void updateBattleFieldGrid(){
        gridpBattlefield.getChildren().clear();
        for(int i = 0; i < GameManager.height; i++){
            for(int j = 0; j < GameManager.width; j++){
                gridpBattlefield.add((Node)GameManager.getBattleField().getTiles()[i][j].getPane(),j,i);
            }
        }
    }
    private void unselectInventoryButtons(){
        for(Node node: gridpInventoryParent.getChildren()){
            if(node instanceof Pane) node.getStyleClass().removeAll("selectedInventorySlot");
        }
    }
    private void logUnitMoved(int x, int y){
        Color spellColor = Color.MEDIUMPURPLE;
        Text t1 = new Text("A ");
        Text t2 = new Text(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
        t2.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(0,.4,1,1):new Color(1,0,0,1));
        Text t3 = new Text(" átlépett a ");
        Text t4 = new Text("("+(char)('A'+x)+","+(y+1)+") ");
        t4.setFill(spellColor);
        Text t5 = new Text("mezőre!");
        addBattleLog(t1,t2,t3,t4,t5);
    }
    private void logUnitAttack(int[] outcome, int x2, int y2){
        Color spellColor = Color.MEDIUMPURPLE;
        Text t1 = new Text("Megtámadta a ");
        Text t2 = new Text(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
        t2.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(0,.4,1,1):new Color(1,0,0,1));
        Text t3 = new Text(" a ");
        Text t4 = new Text(GameManager.getBattleField().getTiles()[x2][y2].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
        t4.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(1,0,0,1):new Color(0,.4,1,1));
        Text t5 = new Text("-t amely ");
        Text t6 = new Text("("+outcome[0]+(outcome[2]==1?") [Krit]":")"));
        t6.setFill(spellColor);
        Text t7 = new Text(" egységet pusztított el.");
        addBattleLog(t1,t2,t3,t4,t5,t6,t7);
        if(outcome[1]!=-1){
            Text t8 = new Text("Viszatámadott a ");
            Text t9 = new Text(GameManager.getBattleField().getTiles()[x2][y2].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
            t9.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(1,0,0,1):new Color(0,.4,1,1));
            Text t10 = new Text(" és ");
            Text t11 = new Text("("+outcome[1]+(outcome[2]==1?") [Krit] ":") "));
            t11.setFill(spellColor);
            Text t12 = new Text(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
            t12.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(0,.4,1,1):new Color(1,0,0,1));
            Text t13 = new Text(" egységet pusztított el.");
            addBattleLog(t8,t9,t10,t11,t12,t13);
        }
    }
    private void logHeroAttackOutcome(int kills, int x, int y){
        Color spellColor = Color.MEDIUMPURPLE;
        Text t1 = new Text("A ");
        Text t2 = new Text("HŐS ");
        t2.setFill(GameManager.getBattleStage()==BattleStage.P1ROUND?new Color(0,.4,1,1):new Color(1,0,0,1));
        Text t3 = new Text("megtámadta a ");
        Text t4 = new Text(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
        t4.setFill((GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0])?new Color(0,.4,1,1):new Color(1,0,0,1));
        Text t5 = new Text(" és elpusztított ");
        Text t6 = new Text("("+kills+") ");
        t6.setFill(spellColor);
        Text t7 = new Text("egységet!");
        addBattleLog(t1,t2,t3,t4,t5,t6,t7);
    }
    private void logSpellOutcome(SpellType spellType, int outcome, int x, int y){
        Color spellColor = Color.MEDIUMPURPLE;
        Text t2 = new Text(spellType.inHungarian()+" ");
        t2.setFill(spellColor);
        Text t3 = new Text("képesség használva! ");
        switch (spellType){
            case LIGHTNINGSTRIKE:
                t3 = new Text("használva! ");
                Text t4 = new Text(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
                t4.setFill((GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0])?new Color(0,.4,1,1):new Color(1,0,0,1));
                Text t5 = new Text(" célponton, mely ");
                Text t6 = new Text("("+outcome+") ");
                t6.setFill(spellColor);
                Text t7 = new Text("egységet pusztított el.");
                addBattleLog(t2,t3,t4,t5,t6,t7);
                return;
            case FIREBALL:
                t4 = new Text( "Összesen ");
                t5 = new Text("("+outcome+ ") ");
                t5.setFill(spellColor);
                t6 = new Text("egységet pusztított el.");
                addBattleLog(t2,t3,t4,t5,t6);
                return;
            case RESURRECT:
                t3 = new Text("használva! ");
                t4 = new Text( "Amely ");
                t5 = new Text("("+outcome+ ") ");
                t5.setFill(spellColor);
                t6 = new Text(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
                t6.setFill((GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0])?new Color(0,.4,1,1):new Color(1,0,0,1));
                t7 = new Text(" egységet támasztott fel.");
                addBattleLog(t2,t3,t4,t5,t6,t7);
                return;
            case MAGICSHIELD:
                t4 = new Text( curHero()[0].isPlayer()?"Ellenfeled ":"Te");
                t5 = new Text("("+outcome+ ") ");
                t5.setFill(spellColor);
                t6 = new Text(curHero()[0].isPlayer()?"körig nem tud varázsolni.":"körig nem varászolhatsz");
                addBattleLog(t2,t3,t4,t5,t6);
                return;
            case FREEZE:
                t3 = new Text("használva! ");
                t4 = new Text( "Amely lefagyasztotta  a ");
                t5 = new Text(GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getUnits().get(0).getUnitType().inHungarian());
                t5.setFill((GameManager.getBattleField().getTiles()[x][y].getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0])?new Color(0,.4,1,1):new Color(1,0,0,1));
                t6 = new Text(" egységet ");
                t7 = new Text("("+outcome+ ") ");
                t7.setFill(spellColor);
                Text t8 = new Text(" körre.");
                addBattleLog(t2,t3,t4,t5,t6,t7,t8);
        }
    }
    private void logPlayerTurn(){
        if(firstPlayer || GameManager.isIsPVP()){
            Text headerColored;
            if(firstPlayer){
                headerColored = new Text(" KÉK "+GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
                headerColored.setFill(new Color(0,.4,1,1));
                addBattleLog(new Text("===================="),headerColored,new Text(" köre "),new Text("===================="));
            }
            else{
                headerColored = new Text(" PIROS "+GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType().inHungarian());
                headerColored.setFill(new Color(1,0,0,1));
                addBattleLog(new Text("==================="),headerColored,new Text(" köre "),new Text("==================="));
            }
            int c = 0;
            for(Node node: gridpInventoryParent.getChildren()){
                if(node instanceof Pane && !node.disableProperty().get()) c++;
            }
            addBattleLog(new Text(GameManager.getQueueUnits().get(0).isFreezed()?"Sem lépni, sem támadni nem tudsz mivel le van fagyasztva az egységed.":"Ha lépni szeretnél, vagy támadni akkor kattints a célmezőre."));
            addBattleLog(new Text(c==0?"Nem tudsz varázsolni (manahiány/varázsoltál már/az ellenség megbénított).":"Varázsláshoz válassz képességet és célmezőt"));
            addBattleLog(new Text(curHero()[0].getAttackDelay()>0?curHero()[0].getAttackDelay()+" körig még nem tudsz támadni a hősöddel.":"A hősöddel támadáshoz kattints rá és a célpont mezőre."));
        }
    }
    private void logTacticalStageHelp(){
        Text headerColored;
        if(firstPlayer){
            headerColored = new Text(" KÉK");
            headerColored.setFill(new Color(0,.4,1,1));
            addBattleLog(new Text("===================="),headerColored,new Text(" játékos taktikai köre "),new Text("===================="));
        }
        else if(GameManager.isIsPVP()){
            headerColored = new Text(" PIROS");
            headerColored.setFill(new Color(1,0,0,1));
            addBattleLog(new Text("==================="),headerColored,new Text(" játékos taktikai köre "),new Text("==================="));
        }else{
            headerColored = new Text("SZÁMÍTÓGÉP");
            headerColored.setFill(new Color(1,0,0,1));
            addBattleLog(new Text("================== a "),headerColored,new Text(" taktikai köre "),new Text("=================="));
            addBattleLog(new Text("Az ellenfeled a csúcsszuper számítógép elhelyezte az egységeit."));
            addBattleLog(new Text("Ebben a körben semmit sem csinálhatsz, csak lelkiekben felkészülhetsz."));
            addBattleLog(new Text("Ha szeretnéd megkezdeni az első kört, akkor kattints a kör befejezésére."));
        }
        if(firstPlayer || GameManager.isIsPVP()){
            addBattleLog(new Text("Kattints az egységekre és a kívánt mezőre, hogy lehelyezd őket."));
            addBattleLog(new Text("Egységeid pozícióját variálhatod a jelenlegi és az új mezőjére kattintva."));
            addBattleLog(new Text("Ha úgy érzed készen állsz a csatára, kattints a kör befejezése gombra."));
        }
    }
    private void setPlayerHeroes(){
        labelBlueName.setText("Kék Játékos");
        labelRedName.setText(GameManager.isIsPVP()?"Piros Játékos":"Számítógép");
        imgvBlue.setImage(new Image(App.class.getResource("Images/BluePlayer.png").toString()));
        imgvRed.setImage(new Image(App.class.getResource("Images/RedPlayer.png").toString()));
        Image manaImage = new Image(App.class.getResource("Images/mana.png").toString());
        imgvManaIcon1.setImage(manaImage);
        imgvManaIcon2.setImage(manaImage);
    }
    private void setBattleBackground(){
        Image bg = new Image(App.class.getResource("Images/battlefield.jpg").toString());
        BackgroundImage bgImg = new BackgroundImage(bg, BackgroundRepeat.NO_REPEAT,BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT,BackgroundSize.DEFAULT);
        vboxGodParent.backgroundProperty().set(new Background(bgImg));
    }
    private void setUpBattleField(){
        GameManager.setBattleField(new BattleField(GameManager.height,GameManager.width));
        updateBattleFieldGrid();
    }
    private void setUpInventoryButtons(){
        for(int i = 0; i < gridpInventoryParent.getColumnCount(); i++){
            Pane pane = (Pane)gridpInventoryParent.getChildren().get(i);
            int finalI = i;
            pane.setOnMouseClicked(event ->{
                pane.getStyleClass().add("selectedInventorySlot");
                for(int j = 0; j < gridpInventoryParent.getColumnCount(); j++){
                    Pane cur = (Pane)gridpInventoryParent.getChildren().get(j);
                    if(cur != pane) cur.getStyleClass().removeAll("selectedInventorySlot");
                }
                GameManager.setSelectedUnitType(UnitType.values()[finalI]);
                if(GameManager.getSelectedTile()!=null)deployUnit(GameManager.getSelectedTile().getX(),GameManager.getSelectedTile().getY());
            });
        }
    }
    private void setUpSpellButtons(){
        int i = 0;
        for(SpellType spellType: SpellType.values()){
            //Visuals
            showSpellsInInventory();
            //Function
            Pane pane = (Pane)gridpInventoryParent.getChildren().get(i);
            gridpInventoryParent.getChildren().get(i).setOnMouseClicked(event -> {
                GameManager.setSelectedSpellType(null);
                for(int j = 0; j < gridpInventoryParent.getColumnCount(); j++){
                    Pane cur = (Pane)gridpInventoryParent.getChildren().get(j);
                    if(cur != pane)cur.getStyleClass().removeAll("selectedInventorySlot");
                }
                if(pane.getStyleClass().contains("selectedInventorySlot")){
                    pane.getStyleClass().removeAll("selectedInventorySlot");
                    unsetTilesAfterHeroMove();
                    btnEndTurn.setDisable(false);
                }else{
                    pane.getStyleClass().add("selectedInventorySlot");
                    GameManager.setSelectedSpellType(spellType);
                    GameManager.selectedSpell();
                    setUpTilesForMagic(spellType);
                    btnEndTurn.setDisable(true);
                }
            });
            i++;
        }
    }
    private void setUpUnitBattleTiles(){
        for(BattleField.Tile[] row: GameManager.getBattleField().getTiles()) {
            for (BattleField.Tile tile : row) {
                tile.getPane().setOnMouseEntered(mouseEvent -> {
                    for(int i = 0; i < GameManager.height; i++){
                        for(int j =0; j < GameManager.width; j++) {
                            GameManager.getBattleField().getTiles()[i][j].disselectTile();
                        }
                    }
                    if(tile.isAvailable()) tile.setTileSelected();
                    updateTilesVisuals();
                });
                tile.getPane().setOnMouseClicked(mouseEvent -> {
                    if(!curHero()[0].isUsedUnitThisTurn() && tile.isAvailable()){
                        if(tile.getUnitOnTile() != null && tile.isAvailable() && tile.getUnitOnTile() != GameManager.getQueueUnits().get(0)  ){
                            int[] res = GameManager.unitAttackUnit(tile.getX(), tile.getY());
                            logUnitAttack(res, tile.getX(), tile.getY());
                            if(curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).getHealth() <= 0){
                                GameManager.getBattleField().getTiles()[curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).getX()][curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).getY()].removeUnitFromTile();
                            }
                            if(GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile().getHealth() <= 0){
                                GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].removeUnitFromTile();
                            }
                            setUpBattlefieldTiles();
                            updateBattleFieldGrid();
                            handleGameOver(GameManager.checkForGameOver());
                        }else if(tile.isAvailable() && tile.getUnitOnTile() != GameManager.getQueueUnits().get(0)){
                            int x = tile.getX();
                            int y = tile.getY();
                            GameManager.getBattleField().swapTiles(GameManager.getQueueUnits().get(0).getX(),GameManager.getQueueUnits().get(0).getY(),tile.getX(),tile.getY());
                            GameManager.getQueueUnits().get(0).setX(x);
                            GameManager.getQueueUnits().get(0).setY(y);
                            curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setX(x);
                            curHero()[0].getBattleUnits().get(GameManager.getQueueUnits().get(0).getUnits().get(0).getUnitType()).setY(y);
                            GameManager.getQueueUnits().get(0).setY(y);
                            updateBattleFieldGrid();
                            logUnitMoved(x,y);
                        }
                        curHero()[0].setUsedUnitThisTurn(true);
                        setUpBattlefieldTiles();
                        updateBattleFieldGrid();
                        unsetTilesAfterHeroMove();
                        updateTilesVisuals();
                    }
                });
            }
        }
    }
    private void unsetTilesAfterHeroMove(){
        for(BattleField.Tile[] row: GameManager.getBattleField().getTiles()){
            for(BattleField.Tile tile: row){
                tile.getPane().setOnMouseEntered(event ->{});
                tile.getPane().setOnMouseClicked(event ->{});
                if(tile.getUnitOnTile()!=null && tile.getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0]){
                    tile.setTileBlue();
                }else if( tile.getUnitOnTile()!=null && tile.getUnitOnTile().getHero()[0] == GameManager.getPlayerTwo()[0]){
                    tile.setTileRed();
                }else{
                    tile.setTileNeutral();
                }
                tile.disselectTile();
                tile.setSpellTarget(false);
                if(!curHero()[0].isUsedUnitThisTurn() && GameManager.getBattleStage() != BattleStage.GAMEOVER){
                    GameManager.setUnitAvailableTiles();
                    setUpUnitBattleTiles();
                }else{
                    GameManager.clearTiles();
                }
            }
        }
        setUpHeroButtons();
        showSpellsInInventory();
        updateTilesVisuals();
        btnEndTurn.setDisable(false);
    }
    private void setUpTilesForMagic(SpellType spellType){
        int area = Spell.getSpellArea(spellType);
        for(BattleField.Tile[] row: GameManager.getBattleField().getTiles()){
            for(BattleField.Tile tile: row){
                tile.getPane().setOnMouseEntered(event ->{
                    int startY = Math.max(tile.getX()-area,0);
                    int endY = Math.min(tile.getX()+area,GameManager.height-1);
                    int startX = Math.max(tile.getY()-area,0);
                    int endX = Math.min(tile.getY()+area,GameManager.width-1);
                    for(int i = 0; i < GameManager.height; i++){
                        for(int j =0; j < GameManager.width; j++){
                            if((GameManager.getSelectedSpellType() != SpellType.FREEZE && GameManager.getSelectedSpellType() != SpellType.LIGHTNINGSTRIKE) ||
                                    GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() == null ||
                                    GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] != GameManager.curPlayer()[0]
                            ) {
                                GameManager.getBattleField().getTiles()[i][j].setTileNeutral();
                                GameManager.getBattleField().getTiles()[i][j].setAvailable(true);
                                GameManager.getBattleField().getTiles()[i][j].disselectTile();
                                GameManager.getBattleField().getTiles()[i][j].setSpellTarget(false);
                                if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!=null){
                                    if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] == GameManager.getPlayerOne()[0]){
                                        GameManager.getBattleField().getTiles()[i][j].setTileBlue();
                                    }else{
                                        GameManager.getBattleField().getTiles()[i][j].setTileRed();
                                    }
                                }
                            }
                        }
                    }
                    for (int i = startY; i <= endY; i++) {
                        for (int j = startX; j <= endX; j++) {
                            if ((GameManager.getSelectedSpellType() != SpellType.FREEZE && GameManager.getSelectedSpellType() != SpellType.LIGHTNINGSTRIKE) ||
                                    GameManager.getBattleField().getTiles()[i][j].getUnitOnTile() == null ||
                                    GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] != GameManager.curPlayer()[0]
                            ) {
                                GameManager.getBattleField().getTiles()[i][j].setSpellTarget(true);
                            }
                        }
                    }
                    updateTilesVisuals();
                });
                tile.getPane().setOnMouseClicked(event ->{
                    if (((GameManager.getSelectedSpellType() != SpellType.FREEZE && GameManager.getSelectedSpellType() != SpellType.LIGHTNINGSTRIKE) ||
                            GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile() == null ||
                            GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile().getHero()[0] != GameManager.curPlayer()[0])
                    ) {
                        if(((GameManager.getSelectedSpellType() == SpellType.FREEZE || GameManager.getSelectedSpellType() == SpellType.RESURRECT || GameManager.getSelectedSpellType() == SpellType.LIGHTNINGSTRIKE)
                                && (GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile() != null))
                                || GameManager.getSelectedSpellType() == SpellType.MAGICSHIELD || GameManager.getSelectedSpellType() == SpellType.FIREBALL
                        ){
                            logSpellOutcome(spellType, GameManager.castSpell(spellType, tile.getX(), tile.getY()), tile.getX(), tile.getY());
                            if(GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile().getHero()[0].getBattleUnits().get(GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile().getUnits().get(0).getUnitType()).getHealth() <= 0){
                                GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].removeUnitFromTile();
                            }
                            unsetTilesAfterHeroMove();
                            setUpSpellButtons();
                            unselectInventoryButtons();
                            updateMana();
                            setUpBattlefieldTiles();
                            updateBattleFieldGrid();
                            updateTilesVisuals();
                            handleGameOver(GameManager.checkForGameOver());
                        }
                    }
                });
            }
        }
    }
    private void setUpTilesForHeroAttack(){
        for(BattleField.Tile[] row: GameManager.getBattleField().getTiles()) {
            for (BattleField.Tile tile : row) {
                tile.getPane().setOnMouseEntered(mouseEvent -> {
                    for(int i = 0; i < GameManager.height; i++){
                        for(int j =0; j < GameManager.width; j++){
                            GameManager.getBattleField().getTiles()[i][j].setSpellTarget(false);
                            GameManager.getBattleField().getTiles()[i][j].disselectTile();
                        }
                    }
                    tile.setSpellTarget(true);
                    tile.setTileSelected();
                    updateTilesVisuals();
                });
                tile.getPane().setOnMouseClicked(mouseEvent -> {
                    if(tile.getUnitOnTile()!=null && tile.getUnitOnTile().getHero()[0] != curHero()[0]){
                        logHeroAttackOutcome(GameManager.heroAttack(tile.getX(),tile.getY()),tile.getX(),tile.getY());
                        unsetTilesAfterHeroMove();
                        updateTilesVisuals();
                        labelBlueName.getStyleClass().removeAll("selectedHero");
                        labelRedName.getStyleClass().removeAll("selectedHero");
                        if(GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].getUnitOnTile().getHealth() <= 0){
                            GameManager.getBattleField().getTiles()[tile.getX()][tile.getY()].removeUnitFromTile();
                        }
                        setUpBattlefieldTiles();
                        updateBattleFieldGrid();
                        handleGameOver(GameManager.checkForGameOver());
                    }
                });
            }
        }
    }
    private void setUpInventorySlotsArray(){
        inventorySlots = new Slot[]{
          new Slot(labelInventoryTitle1,labelInventoryCounter1,imgvInventory1),
                new Slot(labelInventoryTitle2,labelInventoryCounter2,imgvInventory2),
                new Slot(labelInventoryTitle3,labelInventoryCounter3,imgvInventory3),
                new Slot(labelInventoryTitle4,labelInventoryCounter4,imgvInventory4),
                new Slot(labelInventoryTitle5,labelInventoryCounter5,imgvInventory5),
                new Slot(labelInventoryTitle6,labelInventoryCounter6,imgvInventory6)
        };
    }
    private void showSpellsInInventory(){
        int i = 0;
        for(SpellType spellType: SpellType.values()){
            inventorySlots[i].getIcon().setImage(new Image(App.class.getResource("Images/"+spellType.toString().toLowerCase()+".png").toString()));
            inventorySlots[i].getTitle().setText(spellType.inHungarian());
            inventorySlots[i].getCounter().setText(String.valueOf(Spell.getSpellManaCost(spellType)));
            Hero enemy = GameManager.getBattleStage()==BattleStage.P1ROUND?GameManager.getPlayerTwo()[0]:GameManager.getPlayerOne()[0];
            if(GameManager.getBattleStage()==BattleStage.GAMEOVER || (enemy.getMagicShielded() > 0) || (curHero()[0].getMana()<Spell.getSpellManaCost(spellType)) || !curHero()[0].getAvailableSpells().get(spellType) || curHero()[0].getSpellDelay()!=0 || !curHero()[0].isPlayer()) gridpInventoryParent.getChildren().get(i).setDisable(true);
            else gridpInventoryParent.getChildren().get(i).setDisable(false);
            i++;
        }
    }
    private void showUnitsInInventory(){
        int i = 0;
        for(UnitType unitType: UnitType.values()){
            inventorySlots[i].getTitle().setText(unitType.inHungarian());
            inventorySlots[i].getIcon().setImage(new Image(App.class.getResource("Images/"+unitType.toString().toLowerCase()+".png").toString()));
            inventorySlots[i].getCounter().setText(String.valueOf(curHero()[0].getUnits().get(unitType).size()));
            if(curHero()[0].getUnits().get(unitType).size()==0 || (!firstPlayer && !GameManager.isIsPVP())){
                gridpInventoryParent.getChildren().get(i).disableProperty().set(true);
            }else{
                gridpInventoryParent.getChildren().get(i).disableProperty().set(false);
            }
            i++;
        }
    }
    private void setUpBattlefieldTiles(){
        for(int i = 0; i < GameManager.height; i++){
            for( int j = 0; j < GameManager.width; j++){
                final int fi = i,fj = j;
                GameManager.getBattleField().getTiles()[i][j].getPane().onMouseClickedProperty().set( event ->{
                    selectTile(fi,fj);
                });
            }
        }
    }
    private void setUpHeroButtons(){
        if(curHero()[0].getAttackDelay() == 0 && GameManager.getBattleStage()!=BattleStage.GAMEOVER && GameManager.curPlayer()[0].isPlayer()){
            if(GameManager.getBattleStage()==BattleStage.P1ROUND){
                imgvBlue.setOnMouseClicked(event ->{
                    setUpHeroButton(imgvBlue, labelBlueName);
                });
            }else{
                imgvRed.setOnMouseClicked(event ->{
                    setUpHeroButton(imgvRed, labelRedName);
                });
            }
        }else{
            if(GameManager.getBattleStage()==BattleStage.P1ROUND){
                imgvBlue.setOnMouseClicked(event ->{});
                labelBlueName.getStyleClass().removeAll("selectedHero");
            }else{
                imgvRed.setOnMouseClicked(event ->{});
                labelRedName.getStyleClass().removeAll("selectedHero");
            }
        }
        if(GameManager.getBattleStage()==BattleStage.P1ROUND){
            imgvRed.setOnMouseClicked(event ->{});
            labelRedName.getStyleClass().removeAll("selectedHero");
        }else{
            imgvBlue.setOnMouseClicked(event ->{});
            labelBlueName.getStyleClass().removeAll("selectedHero");
        }
    }
    private void setUpHeroButton(ImageView imgv, Label label){
        if(label.getStyleClass().contains("selectedHero")){
            label.getStyleClass().removeAll("selectedHero");
            GameManager.setUnitAvailableTiles();
            unsetTilesAfterHeroMove();
        }else{
            label.getStyleClass().add("selectedHero");
            GameManager.clearTiles();
            if(curHero()[0].getAttackDelay() == 0){
                for(int i = 0; i < GameManager.height; i++){
                    for( int j = 0; j < GameManager.width; j++){
                        if(GameManager.getBattleField().getTiles()[i][j].getUnitOnTile()!= null
                                && GameManager.getBattleField().getTiles()[i][j].getUnitOnTile().getHero()[0] != curHero()[0]) {
                            GameManager.getBattleField().getTiles()[i][j].setAvailable(true);
                        }
                    }
                }
            }
            setUpTilesForHeroAttack();
        }
        updateTilesVisuals();
    }
    private Hero[] curHero(){
        if(GameManager.getBattleStage()!= BattleStage.P1ROUND && GameManager.getBattleStage()!=BattleStage.P2ROUND){
            if(firstPlayer) return GameManager.getPlayerOne();
            return GameManager.getPlayerTwo();
        }else{
            if(GameManager.getBattleStage()== BattleStage.P1ROUND) {
                firstPlayer  = true;
                return GameManager.getPlayerOne();
            }else{
                firstPlayer = false;
                return GameManager.getPlayerTwo();
            }
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        GameManager.getPlayerOne()[0].setUpBattleUnits();
        GameManager.getPlayerTwo()[0].setUpBattleUnits();
        firstPlayer = true;
        GameManager.setUpMana();
        setPlayerHeroes();
        setBattleBackground();
        setUpInventorySlotsArray();
        setUpBattleField();
        setUpInventoryButtons();
        showUnitsInInventory();
        GameManager.nextBattleStage();
        setUpBattlefieldTiles();
        logTacticalStageHelp();
        btnEndTurn.setDisable(true);
        updateUnitsQueue();
        updateRoundLabel();
        updateMana();
    }
}
