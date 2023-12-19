package Heroes;

import Heroes.Enums.TileState;
import Heroes.Units.BattleUnit;
import Heroes.Units.Unit;
import javafx.geometry.Insets;
import javafx.geometry.Point3D;
import javafx.scene.Node;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;

import java.util.List;

/**
 * A csatamezőt tömbösen megvalósító osztály, mely a mezőkkel elvégezhető alapvető metódusokat valósítja meg.
 * Emellett a mezőn lévő grafikus elemeket és egyéb adatokat tartalmaz.
 * Az osztály nem valósítja meg a grafikus megjelenést.
 */
public class BattleField {

    public static class Tile{
        private int x;
        private int y;

        public void setX(int x) {
            this.x = x;
        }
        public void setY(int y) {
            this.y = y;
        }

        private final Pane pane;
        private final ImageView imgv;
        private Label label;
        private BattleUnit unitOnTile;
        private boolean available = false;
        private TileState tileState;
        private boolean isSelected = false;
        private boolean spellTarget;

        public boolean isSpellTarget() {
            return spellTarget;
        }
        public Label getLabel() {
            return label;
        }
        public ImageView getImgv() {
            return imgv;
        }
        public TileState getTileState() {
            return tileState;
        }
        public boolean isSelected() {
            return isSelected;
        }
        public BattleUnit getUnitOnTile() {
            return unitOnTile;
        }
        public void setAvailable(boolean available) {
            this.available = available;
            updateTileStyle();
        }
        public boolean isAvailable() {
            return available;
        }
        public int getX(){
            return x;
        }
        public int getY(){
            return y;
        }

        public Pane getPane(){
            return pane;
        }
        public void addUnitToTile(BattleUnit unit, boolean lookLeft){
            unitOnTile = unit;
            imgv.setImage(new Image(getClass().getResource("Images/"+unit.getUnits().get(0).getUnitType().toString().toLowerCase()+".png").toString()));
            imgv.setFitWidth(65);
            imgv.setFitHeight(65);
            if(lookLeft) {
                imgv.rotationAxisProperty().set(new Point3D(0,1,0));
                imgv.rotateProperty().set(180);
            }
            imgv.setVisible(true);
            setUpLabel();
        }
        public void removeUnitFromTile(){
            pane.getChildren().clear();
            unitOnTile= null;
            imgv.setVisible(false);
            label = null;
            setTileNeutral();
            disselectTile();
        }

        public void setSpellTarget(boolean spellTarget) {
            this.spellTarget = spellTarget;
            updateTileStyle();
        }
        public void setTileRed(){
            tileState = TileState.RED;
            updateTileStyle();
        }
        public void setTileBlue(){
            tileState = TileState.BLUE;
            updateTileStyle();
        }
        public void setTileNeutral(){
            tileState = TileState.NEUTRAL;
            updateTileStyle();
        }
        public void setTileSelected(){
            isSelected = true;
            updateTileStyle();
        }
        public void disselectTile(){isSelected = false; updateTileStyle();}
        public void setUpLabel(){
            if(unitOnTile != null){
                label = new Label(unitOnTile.getUnitsAlive()+"");
                label.getStyleClass().add("unitHealth");
                label.setLayoutX(20);
                label.setLayoutY(40);
                pane.getChildren().add(label);
            }
        }
        public void updateLabel(){
            if(label != null) label.setText(getUnitOnTile().getUnitsAlive()+"");
        }

        public void updateTileStyle(){
            switch (tileState){
                case RED:
                    if(available){
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("redTileAvailable");
                    }else{
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("redTile");
                    }
                    break;
                case BLUE:
                    if(available){
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("blueTileAvailable");
                    }else{
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("blueTile");
                    }
                    break;
                case NEUTRAL:
                    if(available){
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("neutralTileAvailable");
                    }else{
                        pane.getStyleClass().removeAll();
                        pane.getStyleClass().add("neutralTile");
                    }
                    break;
            }
            if(isSelected){
                pane.getStyleClass().add("selectedTile");
            }else{
                pane.getStyleClass().removeAll("selectedTile");
            }
            if(spellTarget){
                pane.getStyleClass().add("spellTargetTile");
            }else{
                pane.getStyleClass().removeAll("spellTargetTile");
            }
        }

        public Tile(int x, int y){
            this.x = x;
            this.y = y;
            pane = new Pane();
            imgv = new ImageView();
            pane.getChildren().add((Node)imgv);
            tileState = TileState.NEUTRAL;
            unitOnTile = null;
            isSelected = false;
            spellTarget = false;
        }
    }

    private final Tile[][] tiles;

    public Tile[][] getTiles(){
        return tiles;
    }
    public void setTile(Tile tile,int x, int y){
        tiles[x][y] = tile;
    }

    public void swapTiles(int x1, int y1, int x2, int y2){
        Tile tmp = tiles[x1][y1];
        tiles[x1][y1] = tiles[x2][y2];
        tiles[x2][y2] = tmp;
        tiles[x1][y1].setX(x1);
        tiles[x1][y1].setY(y1);
        tiles[x2][y2].setX(x2);
        tiles[x2][y2].setY(y2);
    }

    public BattleField(int height, int width){
        height = Math.max(0,height);
        width = Math.max(0,width);
        if(width == 0 && height == 0) {
            tiles = null;
        }else{
            tiles = new Tile[height][width];
        }
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){
                tiles[i][j] = new Tile(i,j);
                tiles[i][j].setTileNeutral();
            }
        }
    }
}
