using UnityEngine;

public abstract class ScriptableAbility : ScriptableObject
{
    public string combo = "";
    public new string name = "ability #1";
    public float staminaCost = 0;
    public float energyCost = 0;
    public AnimationClip animationClip = null;

    public abstract void ApplyPhaseEffects(Entity entity, int phase);
}
