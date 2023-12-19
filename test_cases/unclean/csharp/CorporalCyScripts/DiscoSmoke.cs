using UnityEngine;

public class DiscoSmoke : MonoBehaviour
{
    public SpriteMask mask;
    public Sprite primary;
    public Sprite secondary;

    public void SetSecondarySprite()
    {
        mask.sprite = secondary;
    }

    public void SetPrimarySprite()
    {
        mask.sprite = primary;
    }
}
