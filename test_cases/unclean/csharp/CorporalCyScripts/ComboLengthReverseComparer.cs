using System.Collections.Generic;

public class ComboLengthReverseComparer : IComparer<ScriptableAbility>
{
    public int Compare(ScriptableAbility x, ScriptableAbility y)
    {
        if(x == null || y == null) return 0;
        if(x.combo.Length == y.combo.Length) return 0;
        if(x.combo.Length < y.combo.Length) return 1;
        return -1;
    }
}
