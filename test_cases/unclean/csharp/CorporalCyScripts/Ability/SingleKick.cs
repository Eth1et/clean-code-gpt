using UnityEngine;

[CreateAssetMenu(fileName = "New Ability", menuName = "Ability/SingleKick")]
public class SingleKick : ScriptableAbility
{
    public override void ApplyPhaseEffects(Entity entity, int phase)
    {
        Debug.Log(name + " " + phase);
    }
}
