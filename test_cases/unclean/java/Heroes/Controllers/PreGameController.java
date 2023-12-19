package Heroes.Controllers;


import Heroes.*;
import Heroes.Enums.AIType;
import Heroes.Enums.SpellType;
import Heroes.Enums.StatType;
import Heroes.Enums.UnitType;
import Heroes.Spells.Spell;
import Heroes.Units.Unit;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.URL;
import java.util.*;

/**
 * A csatapontok elosztásáért, annak felületéért felelős osztály
 */
public class PreGameController implements Initializable {
    private Stage stage;
    private Scene scene;
    private Parent root;
    private boolean firstPlayer;
    private int spentSkillPoints;

    @FXML
    private Button btnRES,btnFZ,btnFB,btnLS,btnMS;
    @FXML
    private Button btnPeasentBuy,btnPeasentSell,btnArcherBuy,btnArcherSell,btnGriffBuy,btnGriffSell,btnKentaurBuy,btnKentaurSell,btnGolemBuy,btnGolemSell;
    @FXML
    private Button btnAttackDec,btnAttackInc,btnBack,btnDefenseDec,btnDefenseInc,btnKnowledgeDec;
    @FXML
    private Button btnKnowledgeInc,btnLuckDec,btnLuckInc,btnMagicDec,btnMagicInc,btnMoralDec,btnMoralInc,btnNext;
    @FXML
    private Label labelPeasentPrice,labelArcherPrice,labelGriffPrice,labelKentaurPrice,labelGolemPrice;
    @FXML
    private Label labelResurrect,labelMagicShield,labelFreeze,labelFireball,labelLightningStrike,labelSkillpointPrice;
    @FXML
    private Label labelAttack,labelDefense,labelGold,labelKnowledge,labelLuck,labelMagic,labelMoral,labelText,labelCurPlayer;
    @FXML
    private Label labelPeasentStatText,labelPeasentStats,labelArcherStatText,labelArcherStats,labelGriffStatText,labelGriffStats;
    @FXML
    private Label labelKentaurStatText,labelKentaurStats,labelGolemStatText,labelGolemStats, labelLSMana, labelFBMana, labelRESMana,labelFZMana,labelMSMana;
    @FXML
    private TextField textfieldArcher,textfieldGolem,textfieldGriff,textfieldKentaur,textfieldPeasant;

    @FXML
    void decAttack(ActionEvent event) {
        if(curHero()[0].getAttack()>1){
            curHero()[0].setAttack(curHero()[0].getAttack()-1);
            updateAttack();
            soldSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void decDefense(ActionEvent event) {
        if(curHero()[0].getDefense()>1){
            curHero()[0].setDefense(curHero()[0].getDefense()-1);
            updateDefense();
            soldSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void decKnowledge(ActionEvent event) {
        if(curHero()[0].getKnowledge()>1){
            curHero()[0].setKnowledge(curHero()[0].getKnowledge()-1);
            updateKnowledge();
            soldSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void decLuck(ActionEvent event) {
        if(curHero()[0].getLuck()>1){
            curHero()[0].setLuck(curHero()[0].getLuck()-1);
            updateLuck();
            soldSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void decMagic(ActionEvent event) {
        if(curHero()[0].getMagic()>1){
            curHero()[0].setMagic(curHero()[0].getMagic()-1);
            updateMagic();
            soldSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void decMoral(ActionEvent event) {
        if(curHero()[0].getMoral()>1){
            curHero()[0].setMoral(curHero()[0].getMoral()-1);
            updateMoral();
            soldSkillPoint();
            updateMoney();
        }
    }

    @FXML
    void incAttack(ActionEvent event) {
        if(curHero()[0].getAttack()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
            curHero()[0].setAttack(curHero()[0].getAttack()+1);
            updateAttack();
            boughtSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void incDefense(ActionEvent event) {
        if(curHero()[0].getDefense()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
           curHero()[0].setDefense(curHero()[0].getDefense()+1);
            updateDefense();
            boughtSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void incKnowledge(ActionEvent event) {
        if(curHero()[0].getKnowledge()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
            curHero()[0].setKnowledge(curHero()[0].getKnowledge()+1);
            updateKnowledge();
            boughtSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void incLuck(ActionEvent event) {
        if( curHero()[0].getLuck()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
            curHero()[0].setLuck(curHero()[0].getLuck()+1);
            updateLuck();
            boughtSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void incMagic(ActionEvent event) {
        if( curHero()[0].getMagic()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
            curHero()[0].setMagic(curHero()[0].getMagic()+1);
            updateMagic();
            boughtSkillPoint();
            updateMoney();
        }
    }
    @FXML
    void incMoral(ActionEvent event) {
        if(curHero()[0].getMoral()<10 && curHero()[0].getMoney()>=getPrice(spentSkillPoints+1)){
            curHero()[0].setMoral(curHero()[0].getMoral()+1);
            updateMoral();
            boughtSkillPoint();
            updateMoney();
        }
    }

    private void boughtSkillPoint(){
        spentSkillPoints++;
        updateSkillpointPrice();
        curHero()[0].setMoney(curHero()[0].getMoney()-getPrice(spentSkillPoints));
        updateSkillpointPrice();
        updateSkillpointPrice();
    }
    private void soldSkillPoint(){
        curHero()[0].setMoney(curHero()[0].getMoney()+getPrice(spentSkillPoints));
        spentSkillPoints--;
        updateSkillpointPrice();
        updateSkillpointPrice();
    }

    private void buyOrSellSpell(SpellType spellType){
        Hero[] hero = curHero();
        if(hero[0].getAvailableSpells().get(spellType)){
            hero[0].removeSpell(spellType);
            hero[0].setMoney(hero[0].getMoney()+ Spell.getSpellCost(spellType));
            spellButton(spellType).setText("Vásárlás");
            spellLabel(spellType).setTextFill(Color.RED);
        }else{
            if(hero[0].getMoney() >= Spell.getSpellCost(spellType)){
                hero[0].addSpell(spellType);
                hero[0].setMoney(hero[0].getMoney()-Spell.getSpellCost(spellType));
                spellButton(spellType).setText("Eladás");
                spellLabel(spellType).setTextFill(Color.GREEN);
            }
        }
        updateMoney();
    }

    public Button spellButton(SpellType spellType){
        switch(spellType) {
            case FREEZE:
                return btnFZ;
            case FIREBALL:
                return btnFB;
            case RESURRECT:
                return btnRES;
            case MAGICSHIELD:
                return btnMS;
            case LIGHTNINGSTRIKE:
                return btnLS;
        }
        return null;
    }
    public Label spellLabel(SpellType spellType){
        switch(spellType) {
            case FREEZE:
                return labelFreeze;
            case FIREBALL:
                return labelFireball;
            case RESURRECT:
                return labelResurrect;
            case MAGICSHIELD:
                return labelMagicShield;
            case LIGHTNINGSTRIKE:
                return labelLightningStrike;
        }
        return null;
    }
    public void setUpSpellPrices(){
        labelFireball.setText(String.valueOf(Spell.getSpellCost(SpellType.FIREBALL)));
        labelFreeze.setText(String.valueOf(Spell.getSpellCost(SpellType.FREEZE)));
        labelResurrect.setText(String.valueOf(Spell.getSpellCost(SpellType.RESURRECT)));
        labelMagicShield.setText(String.valueOf(Spell.getSpellCost(SpellType.MAGICSHIELD)));
        labelLightningStrike.setText(String.valueOf(Spell.getSpellCost(SpellType.LIGHTNINGSTRIKE)));
    }

    @FXML
    void buyOrSellFB(ActionEvent event) {
        buyOrSellSpell(SpellType.FIREBALL);
    }
    @FXML
    void buyOrSellFZ(ActionEvent event) {
        buyOrSellSpell(SpellType.FREEZE);
    }
    @FXML
    void buyOrSellLS(ActionEvent event) {
        buyOrSellSpell(SpellType.LIGHTNINGSTRIKE);
    }
    @FXML
    void buyOrSellMS(ActionEvent event) {
        buyOrSellSpell(SpellType.MAGICSHIELD);
    }
    @FXML
    void buyOrSellRES(ActionEvent event) {
        buyOrSellSpell(SpellType.RESURRECT);
    }

    private void setUpUnitStats(){
        String statText = "életerő:\nsebzés:\nsebesség:\nkezdeményezés:";
        labelPeasentStatText.setText(statText);
        labelArcherStatText.setText(statText);
        labelGriffStatText.setText(statText);
        labelKentaurStatText.setText(statText);
        labelGolemStatText.setText(statText);
        labelPeasentStats.setText(getUnitStats(UnitType.PEASANT));
        labelArcherStats.setText(getUnitStats(UnitType.ARCHER));
        labelGriffStats.setText(getUnitStats(UnitType.GRIFF));
        labelKentaurStats.setText(getUnitStats(UnitType.KENTAUR));
        labelGolemStats.setText(getUnitStats(UnitType.GOLEM));
        labelPeasentPrice.setText(Unit.getUnitPrice(UnitType.PEASANT)+"");
        labelArcherPrice.setText(Unit.getUnitPrice(UnitType.ARCHER)+"");
        labelGriffPrice.setText(Unit.getUnitPrice(UnitType.GRIFF)+"");
        labelKentaurPrice.setText(Unit.getUnitPrice(UnitType.KENTAUR)+"");
        labelGolemPrice.setText(Unit.getUnitPrice(UnitType.GOLEM)+"");
    }
    private String getUnitStats(UnitType unitType){
        Unit unit = new Unit(unitType);
        return String.join("\n",unit.getHealth()+"",unit.getMinDamage() + "-" + unit.getMaxDamage(),unit.getSpeed()+"",unit.getInitiative()+"");
    }

    private void buyUnit(UnitType unitType){
        if(curHero()[0].getMoney()>=Unit.getUnitPrice(unitType)){
            curHero()[0].addUnit(unitType);
            curHero()[0].setMoney(curHero()[0].getMoney()-Unit.getUnitPrice(unitType));
            updateAll();
        }
    }
    private void sellUnit(UnitType unitType){
        if(curHero()[0].getUnits().get(unitType).size()>0){
            curHero()[0].removeUnit(unitType);
            curHero()[0].setMoney(curHero()[0].getMoney()+Unit.getUnitPrice(unitType));
            updateAll();
        }
    }

    @FXML
    void buyArcher(ActionEvent event) {
        buyUnit(UnitType.ARCHER);
    }
    @FXML
    void buyGolem(ActionEvent event) {
        buyUnit(UnitType.GOLEM);
    }
    @FXML
    void buyGriff(ActionEvent event) {
        buyUnit(UnitType.GRIFF);
    }
    @FXML
    void buyKentaur(ActionEvent event) {
        buyUnit(UnitType.KENTAUR);
    }
    @FXML
    void buyPeasent(ActionEvent event) {
        buyUnit(UnitType.PEASANT);
    }

    @FXML
    void sellArcher(ActionEvent event) {
        sellUnit(UnitType.ARCHER);
    }
    @FXML
    void sellGolem(ActionEvent event) {
        sellUnit(UnitType.GOLEM);
    }
    @FXML
    void sellGriff(ActionEvent event) {
        sellUnit(UnitType.GRIFF);
    }
    @FXML
    void sellKentaur(ActionEvent event) {
        sellUnit(UnitType.KENTAUR);
    }
    @FXML
    void sellPeasent(ActionEvent event) {
        sellUnit(UnitType.PEASANT);
    }

    private void setUpManaLabels(){
        labelLSMana.setText(Spell.getSpellManaCost(SpellType.LIGHTNINGSTRIKE)+" mana");
        labelFBMana.setText(Spell.getSpellManaCost(SpellType.FIREBALL)+" mana");
        labelRESMana.setText(Spell.getSpellManaCost(SpellType.RESURRECT)+" mana");
        labelMSMana.setText(Spell.getSpellManaCost(SpellType.MAGICSHIELD)+" mana");
        labelFZMana.setText(Spell.getSpellManaCost(SpellType.FREEZE)+" mana");
    }

    private void setUpPlayerText(){
        if(!firstPlayer){
            labelCurPlayer.setText(curHero()[0].isPlayer()?"Piros Játékos":"Számítógép");
            labelCurPlayer.setTextFill(Color.DARKRED);
        }else{
            labelCurPlayer.setText("Kék Játékos");
            labelCurPlayer.setTextFill(Color.DARKBLUE);
        }
    }

    private void generateEnemy(){
        Random rnd = new Random();
        GameManager.setAiType(AIType.values()[rnd.nextInt(4)]);
        switch(GameManager.getAiType()){
            case ELF:
                elfDistribute();
                break;
            case LANDLORD:
                landlordDistribute();
                break;
            case WIZARD:
                wizardDistribute();
                break;
            case ARCHERMASTER:
                archermasterDistribute();
                break;
        }
    }
    public void wizardDistribute(){
        Random rnd = new Random();
        int attack = 1+rnd.nextInt(2);
        int magic = 6+rnd.nextInt(3);
        int knowledge = 6+rnd.nextInt(3);
        int spellCount = 3+rnd.nextInt(2);
        int unitCount = 2+rnd.nextInt(2);

        incStatToX(StatType.ATTACK,attack);
        incStatToX(StatType.MAGIC,magic);
        incStatToX(StatType.KNOWLEDGE,knowledge);
        buyNSpells(spellCount);
        buyUnitsRandomlyUntilOutOfMoney(getUnownedUnits(unitCount,new UnitType[0]));
    }
    public void elfDistribute(){
        Random rnd = new Random();
        int attack = 3 + rnd.nextInt(3);
        int spellcount = 2;
        int unitCount = 2 + rnd.nextInt(2);

        incStatToX(StatType.ATTACK, attack);
        for(StatType type: new StatType[] {StatType.DEFENSE,StatType.KNOWLEDGE,StatType.MORAL,StatType.MAGIC,StatType.LUCK}){
            incStatToX(type,2+rnd.nextInt(3));
        }
        buyNSpells(2);
        buyUnitsRandomlyUntilOutOfMoney(getUnownedUnits(unitCount,new UnitType[]{UnitType.PEASANT,UnitType.ARCHER}));
    }
    public void landlordDistribute(){
        Random rnd = new Random();
        int attack = 5 + rnd.nextInt(4);
        int defense = 5 + rnd.nextInt(4);
        int moral = 3 + rnd.nextInt(4);
        int luck = 1 + rnd.nextInt(3);
        int unitCount = 1 + rnd.nextInt(2);

        incStatToX(StatType.ATTACK,attack);
        incStatToX(StatType.DEFENSE,defense);
        incStatToX(StatType.MORAL,moral);
        incStatToX(StatType.LUCK,luck);
        buyOrSellSpell(SpellType.MAGICSHIELD);
        if(unitCount == 1){
            buyUnitsRandomlyUntilOutOfMoney(new UnitType[]{UnitType.PEASANT});
        }else{
            buyUnitsRandomlyUntilOutOfMoney(new UnitType[]{UnitType.PEASANT,UnitType.ARCHER});
        }
    }
    public void archermasterDistribute(){
        Random rnd = new Random();
        int attack = 5 + rnd.nextInt(4);
        int defense = 2 + rnd.nextInt(3);
        int moral = 1 + rnd.nextInt(3);
        int luck = 3 + rnd.nextInt(3);
        int unitCount = 1 + rnd.nextInt(2);

        incStatToX(StatType.ATTACK,attack);
        incStatToX(StatType.DEFENSE,defense);
        incStatToX(StatType.MORAL,moral);
        incStatToX(StatType.LUCK,luck);
        buyOrSellSpell(SpellType.RESURRECT);
        buyOrSellSpell(SpellType.FREEZE);
        if(unitCount == 1){
            buyUnitsRandomlyUntilOutOfMoney(new UnitType[]{UnitType.ARCHER});
        }else{
            buyUnitsRandomlyUntilOutOfMoney(new UnitType[]{UnitType.ARCHER,UnitType.KENTAUR});
        }
    }

    private void setUnitNumber(UnitType type){
        int n = curHero()[0].getUnits().get(type).size();
        int p = curHero()[0].getUnits().get(type).size();
        try{
            switch (type){
                case ARCHER:
                    n = Integer.parseInt(textfieldArcher.getText());
                    break;
                case KENTAUR:
                    n = Integer.parseInt(textfieldKentaur.getText());
                    break;
                case GOLEM:
                    n = Integer.parseInt(textfieldGolem.getText());
                    break;
                case GRIFF:
                    n = Integer.parseInt(textfieldGriff.getText());
                    break;
                case PEASANT:
                    n = Integer.parseInt(textfieldPeasant.getText());
                    break;
            }
            if(n > p && (n-p)*Unit.getUnitPrice(type) > curHero()[0].getMoney()){
                n = curHero()[0].getUnits().get(type).size() + curHero()[0].getMoney()/Unit.getUnitPrice(type);
            }
            if(n < 0) n = 0;
            if(n < p){
                for(int i = 0; i < Math.abs(p-n);i++){
                    sellUnit(type);
                }
            }else{
                for(int i = 0; i < n-p;i++){
                    buyUnit(type);
                }
            }
        }catch(Exception e){
            System.out.println("Rossz bemenet!: nem egész szám");
        }
        updateAll();
    }

    @FXML
    void setArcherNumber(ActionEvent event) {
        setUnitNumber(UnitType.ARCHER);
    }
    @FXML
    void setGolemNumber(ActionEvent event) {
        setUnitNumber(UnitType.GOLEM);
    }
    @FXML
    void setGriffNumber(ActionEvent event) {
        setUnitNumber(UnitType.GRIFF);
    }
    @FXML
    void setKentaurNumber(ActionEvent event) {
        setUnitNumber(UnitType.KENTAUR);
    }
    @FXML
    void setPeasantNumber(ActionEvent event) {
        setUnitNumber(UnitType.PEASANT);
    }

    private void incStatToX(StatType statType, int goal){
        for(int i = 1; i < goal; i++){
            switch(statType){
                case LUCK:
                    incLuck(new ActionEvent());
                    break;
                case MAGIC:
                    incMagic(new ActionEvent());
                    break;
                case MORAL:
                    incMoral(new ActionEvent());
                    break;
                case ATTACK:
                    incAttack(new ActionEvent());
                    break;
                case DEFENSE:
                    incDefense(new ActionEvent());
                    break;
                case KNOWLEDGE:
                    incKnowledge(new ActionEvent());
                    break;
            }
        }
    }
    private SpellType getUnownedSpell(){
        Random rnd = new Random();
        int checked = rnd.nextInt(curHero()[0].getAvailableSpells().size());
        if(!curHero()[0].getAvailableSpells().get(SpellType.values()[checked])){
            return SpellType.values()[checked];
        }else{
            return getUnownedSpell();
        }
    }
    private void buyNSpells(int n){
        for(int i = 0; i < n; i++){
            buyOrSellSpell(getUnownedSpell());
        }
    }
    private boolean containsUnitType(UnitType[] arr, UnitType searchFor){
        if(arr.length == 0 || searchFor == null) return false;
        for(UnitType unit:arr){
            if(unit.equals(searchFor)){
                return true;
            }
        }
        return false;
    }
    private void buyUnitsRandomlyUntilOutOfMoney(UnitType[] units){
        Random rnd = new Random();
        while(hasMoneyForUnits(units)){
            for(UnitType unit: units){
                if(curHero()[0].getMoney()>=Unit.getUnitPrice(unit) && rnd.nextBoolean()){
                    buyUnit(unit);
                }
            }
        }
    }
    private boolean hasMoneyForUnits(UnitType[] units){
        for(UnitType type: units){
            if(Unit.getUnitPrice(type)<=curHero()[0].getMoney()){
                return true;
            }
        }
        return false;
    }
    private UnitType[] getUnownedUnits(int n, UnitType[] excludedOnes){
        UnitType[] units = new UnitType[Math.min(n,5-excludedOnes.length)];
        for(int i = 0; i < units.length;i++){
            units[i] = getUnownedUnit(excludedOnes);
        }
        return units;
    }
    private UnitType getUnownedUnit(UnitType[] excludedOnes){
        Random rnd = new Random();
        int checked = rnd.nextInt(curHero()[0].getUnits().size());
        if(curHero()[0].getUnits().get(UnitType.values()[checked]).size()==0 && !containsUnitType(excludedOnes, UnitType.values()[checked])){
            return UnitType.values()[checked];
        }else{
            return getUnownedUnit(excludedOnes);
        }
    }

    public void updateAttack(){
        labelAttack.setText(String.valueOf(curHero()[0].getAttack()));
    }
    public void updateDefense(){
        labelDefense.setText(String.valueOf(curHero()[0].getDefense()));
    }
    public void updateKnowledge(){
        labelKnowledge.setText(String.valueOf(curHero()[0].getKnowledge()));
    }
    public void updateMoral(){
        labelMoral.setText(String.valueOf(curHero()[0].getMoral()));
    }
    public void updateLuck(){
        labelLuck.setText(String.valueOf(curHero()[0].getLuck()));
    }
    public void updateMagic(){
        labelMagic.setText(String.valueOf(curHero()[0].getMagic()));
    }
    public void updateMoney(){
        labelGold.setText(String.valueOf(curHero()[0].getMoney()));
    }
    public void updateSkillpointPrice(){
        labelSkillpointPrice.setText(String.valueOf(getPrice(spentSkillPoints+1)));
    }
    public void updatePeasentCount(){
        textfieldPeasant.setText(curHero()[0].getUnits().get(UnitType.PEASANT).size()+"");
    }
    public void updateArcherCount(){
        textfieldArcher.setText(curHero()[0].getUnits().get(UnitType.ARCHER).size()+"");
    }
    public void updateGriffCount(){
        textfieldGriff.setText(curHero()[0].getUnits().get(UnitType.GRIFF).size()+"");
    }
    public void updateKentaurCount(){
        textfieldKentaur.setText(curHero()[0].getUnits().get(UnitType.KENTAUR).size()+"");
    }
    public void updateGolemCount(){
        textfieldGolem.setText(curHero()[0].getUnits().get(UnitType.GOLEM).size()+"");
    }
    public void updateSpentSkillpoints(){
        Hero hero[] = curHero();
        spentSkillPoints = hero[0].getAttack()+hero[0].getDefense()+hero[0].getKnowledge()+hero[0].getLuck()+hero[0].getMoral()+hero[0].getMagic()-6;
        updateSkillpointPrice();
    }
    private void updateSpellStuff(){
        for(SpellType spellType: SpellType.values()){
            if(curHero()[0].getAvailableSpells().get(spellType)){
                spellButton(spellType).setText("Eladás");
                spellLabel(spellType).setTextFill(Color.GREEN);
            }else{
                spellButton(spellType).setText("Vásárlás");
                spellLabel(spellType).setTextFill(Color.RED);
            }
        }
    }
    private void updateTipText(){
        if(curHero()[0].isPlayer()){
            labelText.setText("Oszd el a pénzed taktikusan, hogy felkészülj a csatára!");
        }else{
            labelText.setText("Itt láthatod az ellenfeled ("+GameManager.getAiType().toString()+") csapatját.");
        }
    }
    public void updateAll(){
        updateAttack();
        updateDefense();
        updateKnowledge();
        updateMoral();
        updateLuck();
        updateMagic();
        updateMoney();
        updateSkillpointPrice();
        updateGolemCount();
        updateArcherCount();
        updateKentaurCount();
        updatePeasentCount();
        updateGriffCount();
        updateSpentSkillpoints();
        updateSpellStuff();
        updateTipText();
        btnNext.setDisable(curHero()[0].countUnits()==0);
    }

    private void inputButtonsDisabled(boolean isDisabled){
        List<Button> btns = Arrays.asList(btnAttackInc,btnAttackDec,btnDefenseInc,btnDefenseDec,btnMagicInc,btnMagicDec,btnKnowledgeInc,btnKnowledgeDec,btnMoralInc,btnMoralDec,btnLuckInc,btnLuckDec,
                btnFZ,btnMS,btnFB,btnRES,btnLS,btnPeasentBuy,btnPeasentSell,btnArcherBuy,btnArcherSell,btnGriffBuy,btnGriffSell,btnKentaurBuy,btnKentaurSell,btnGolemBuy,btnGolemSell);
        for(Button btn: btns){
            if(btn!=null)btn.setDisable(isDisabled);
        }
    }

    public Hero[] curHero(){
        if(firstPlayer) return GameManager.getPlayerOne();
        return GameManager.getPlayerTwo();
    }

    public int getPrice(int bySpentPoints){
        int price = 5;
        for(int i = 0; i < bySpentPoints-1; i++){
            price = (int)Math.ceil(price*1.1);
        }
        return price;
    }

    @FXML
    public void goBack(ActionEvent event) throws IOException{
        if(firstPlayer){
            root = FXMLLoader.load(Objects.requireNonNull(App.class.getResource("Scenes/MainMenu.fxml")));
            stage = (Stage)((Node)event.getSource()).getScene().getWindow();
            scene = new Scene(root);
            stage.setScene(scene);
            stage.sizeToScene();
            stage.centerOnScreen();
            stage.show();
        }else{
            if(!GameManager.isIsPVP()){
                GameManager.resetAI();
                spentSkillPoints = 0;
                generateEnemy();
            }else{
                firstPlayer = true;
            }
            setUpPlayerText();
            updateAll();
        }
    }
    @FXML
    void goNext(ActionEvent event) throws IOException{
        if(firstPlayer){
            spentSkillPoints = 0;
            if(!GameManager.isIsPVP()){
                firstPlayer = false;
                generateEnemy();
                inputButtonsDisabled(true);
                btnBack.setText("Újragenerálás");
            }else{
                firstPlayer = false;
            }
            setUpPlayerText();
            updateAll();
        }else{
            root = FXMLLoader.load(Objects.requireNonNull(App.class.getResource("Scenes/Battle.fxml")));
            stage = (Stage)((Node)event.getSource()).getScene().getWindow();
            scene = new Scene(root);
            stage.setScene(scene);
            stage.sizeToScene();
            stage.centerOnScreen();
            stage.show();
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle){
        firstPlayer = true;
        btnBack.setText("Vissza");
        updateAll();
        updateSpentSkillpoints();
        btnBack.setDisable(false);
        btnNext.setDisable(true);
        setUpUnitStats();
        setUpSpellPrices();
        setUpPlayerText();
        inputButtonsDisabled(false);
        setUpManaLabels();
    }
}
