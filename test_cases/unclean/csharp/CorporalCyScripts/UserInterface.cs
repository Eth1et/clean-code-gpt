using UnityEngine;
using UnityEngine.UI;

public class UserInterface : MonoBehaviour
{
    [SerializeField] private Text fpsText;
    [SerializeField] private Player player;
    [SerializeField] private ProgressBar healthBar, staminaBar, energyBar;

    [SerializeField] private float hudRefreshRate = 1f;

    private float timer;
    private int fps;

    private void Update()
    {
        if (Time.unscaledTime > timer)
        {
            fps = (int)(1f / Time.unscaledDeltaTime);
            timer = Time.unscaledTime + hudRefreshRate;
            fpsText.text = "FPS: " + fps;
        }

        healthBar.SetProgress(player.Health, player.maxHealth);
        staminaBar.SetProgress(player.Stamina, player.maxStamina);
        energyBar.SetProgress(player.Energy, player.maxEnergy);
    }
}
