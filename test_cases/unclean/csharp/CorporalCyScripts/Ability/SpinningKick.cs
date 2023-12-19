using UnityEngine;

[CreateAssetMenu(fileName = "New Ability", menuName = "Ability/SpinningKick")]
public class SpinningKick : ScriptableAbility
{
    public override void ApplyPhaseEffects(Entity entity, int phase)
    {
        Debug.Log(this.name + " " + phase);
    }
}
