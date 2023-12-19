package Heroes.Tests;
import Heroes.BattleField;
import Heroes.Enums.Difficulty;
import Heroes.GameManager;
import Heroes.Hero;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Teszteli a GameManager osztály bizonyos metódusait
 */
public class TestGameManager {
    @Test
    public void testDifficultyBasedMoney(){
        assertEquals(1300, GameManager.difficultyBasedMoney(Difficulty.EASY));
        assertEquals(1000, GameManager.difficultyBasedMoney(Difficulty.MEDIUM));
        assertEquals(700, GameManager.difficultyBasedMoney(Difficulty.HARD));
    }
    @Test
    public void testClearTilesAndBattlefieldSetterGetterAndBattlefieldSetAvailable(){
        GameManager.setBattleField(new BattleField(10,20));
        for(int i = 0; i <10; i++){
            for(int j = 0; j <20; j++){
                assertFalse(GameManager.getBattleField().getTiles()[i][j].isAvailable());
                assertEquals(i,GameManager.getBattleField().getTiles()[i][j].getX());
                assertEquals(j,GameManager.getBattleField().getTiles()[i][j].getY());
            }
        }
        for(int i = 0; i <10; i++){
            for(int j = 0; j <20; j++){
                GameManager.getBattleField().getTiles()[i][j].setAvailable(true);
                assertTrue(GameManager.getBattleField().getTiles()[i][j].isAvailable());
                assertEquals(i,GameManager.getBattleField().getTiles()[i][j].getX());
                assertEquals(j,GameManager.getBattleField().getTiles()[i][j].getY());
            }
        }

        GameManager.setBattleField(new BattleField(20,22));
        for(int i = 0; i <20; i++){
            for(int j = 0; j <22; j++){
                assertFalse(GameManager.getBattleField().getTiles()[i][j].isAvailable());
                assertEquals(i,GameManager.getBattleField().getTiles()[i][j].getX());
                assertEquals(j,GameManager.getBattleField().getTiles()[i][j].getY());
            }
        }
        for(int i = 0; i <20; i++){
            for(int j = 0; j <22; j++){
                GameManager.getBattleField().getTiles()[i][j].setAvailable(true);
                assertTrue(GameManager.getBattleField().getTiles()[i][j].isAvailable());
                assertEquals(i,GameManager.getBattleField().getTiles()[i][j].getX());
                assertEquals(j,GameManager.getBattleField().getTiles()[i][j].getY());
            }
        }

        GameManager.setBattleField(new BattleField(-1,-1));
        assertNull(GameManager.getBattleField().getTiles());
    }
}
