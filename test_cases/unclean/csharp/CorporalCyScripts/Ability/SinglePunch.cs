using UnityEngine;

[CreateAssetMenu(fileName = "New Ability", menuName = "Ability/SinglePunch")]
public class SinglePunch : ScriptableAbility
{
    public override void ApplyPhaseEffects(Entity entity, int phase)
    {
        Debug.Log(this.name + " " + phase);
    }
}
