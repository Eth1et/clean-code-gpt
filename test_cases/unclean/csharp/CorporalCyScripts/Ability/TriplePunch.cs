using UnityEngine;

[CreateAssetMenu(fileName = "New Ability", menuName = "Ability/TriplePunch")]
public class TriplePunch : ScriptableAbility
{
    public override void ApplyPhaseEffects(Entity entity, int phase)
    {
        Debug.Log(this.name + " " + phase);
    }
}
