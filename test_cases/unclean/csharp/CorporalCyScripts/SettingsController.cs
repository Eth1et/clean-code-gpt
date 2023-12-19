using UnityEngine;

public class SettingsController : MonoBehaviour {

    void Awake()
    {
        Application.targetFrameRate = (int)(Screen.currentResolution.refreshRateRatio.value * 1.05f);
        //Application.targetFrameRate = 30;
    }
}
