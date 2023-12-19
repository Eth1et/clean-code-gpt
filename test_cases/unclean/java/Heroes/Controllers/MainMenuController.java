package Heroes.Controllers;

import Heroes.Enums.Difficulty;
import Heroes.GameManager;
import Heroes.App;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Objects;


/**
 * A főmenü jelenet felhasználói felületéért, annak funkcióiért felelős osztály.
 */
public class MainMenuController {

    @FXML
    private Button btnEasy;
    @FXML
    private Button btnHard;
    @FXML
    private Button btnMedium;
    @FXML
    private Button btnMulti;
    @FXML
    private Button btnQuit;
    @FXML
    private Button btnSingle;
    @FXML
    private Button btnBack;
    @FXML
    private Label labelText;
    @FXML
    private Label labelTextShadow;
    private static Stage stage;
    private static Scene scene;
    private static Parent root;

    public void switchToPreGame(ActionEvent event) throws IOException {
        root = FXMLLoader.load(Objects.requireNonNull(App.class.getResource("Scenes/PreGame.fxml")));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root);
        stage.setScene(scene);
        stage.sizeToScene();
        stage.centerOnScreen();
        stage.show();
    }

    public void btnSingleClicked(){
        GameManager.setIsPVP(false);
        showDifficultyButtons();
    }
    public void btnMultiClicked(){
        GameManager.setIsPVP(true);
        showDifficultyButtons();
    }

    public void showDifficultyButtons(){
        labelText.setText("Válassz Nehézségi Fokozatot!");
        labelTextShadow.setText("Válassz Nehézségi Fokozatot!");
        btnSingle.setDisable(true);
        btnMulti.setDisable(true);
        btnQuit.setDisable(true);
        btnQuit.setOpacity(0);
        btnSingle.setOpacity(0);
        btnMulti.setOpacity(0);
        btnBack.setOpacity(100);
        btnEasy.setOpacity(100);
        btnMedium.setOpacity(100);
        btnHard.setOpacity(100);
        btnBack.setDisable(false);
        btnEasy.setDisable(false);
        btnMedium.setDisable(false);
        btnHard.setDisable(false);
    }

    public void hideDifficultyButtons(){
        labelText.setText("Not Heroes of Not Might & Not Magic");
        labelTextShadow.setText("Not Heroes of Not Might & Not Magic");
        btnBack.setDisable(true);
        btnEasy.setDisable(true);
        btnMedium.setDisable(true);
        btnHard.setDisable(true);
        btnQuit.setOpacity(100);
        btnSingle.setOpacity(100);
        btnMulti.setOpacity(100);
        btnBack.setOpacity(0);
        btnEasy.setOpacity(0);
        btnMedium.setOpacity(0);
        btnHard.setOpacity(0);
        btnSingle.setDisable(false);
        btnMulti.setDisable(false);
        btnQuit.setDisable(false);
    }

    public void btnEasyClicked(ActionEvent event) throws IOException{
        GameManager.initialize(Difficulty.EASY);
        switchToPreGame(event);
    }
    public void btnMediumClicked(ActionEvent event) throws IOException{
        GameManager.initialize(Difficulty.MEDIUM);
        switchToPreGame(event);
    }
    public void btnHardClicked(ActionEvent event) throws IOException{
        GameManager.initialize(Difficulty.HARD);
        switchToPreGame(event);
    }

    public void btnQuitClicked(){
        System.out.println("Kilépés...");
        System.exit(0);
    }
}
