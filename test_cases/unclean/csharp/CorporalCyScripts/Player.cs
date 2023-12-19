using UnityEngine;

public class Player : Entity
{   
    protected override void Awake()
    {
        base.Awake();
    }

    protected override void Start()
    {
        base.Start();
    }
    
    protected override void Update()
    {
        base.Update();

        UpdateInputs();

        if (!inAttack && alive)
        {
            CheckCombatInputs();
        }
    }

    protected override void FixedUpdate()
    {
        base.FixedUpdate();
    }

    protected override void LateUpdate()
    {
        base.LateUpdate();
    }

    private void CheckCombatInputs()
    {
        if(Time.time >= cancelCombo && !combo.Equals(""))
        {
            combo.Clear();
        }
        if(Time.time >= nextAttack)
        {
            int lastComboCount = combo.Length;

            if (Input.GetKeyDown(KeyCode.H))
                combo.Append("L"); // Light
            else if (Input.GetKeyDown(KeyCode.J))
                combo.Append("H"); // Heavy
            else if (Input.GetKeyDown(KeyCode.K))
                combo.Append("S"); // Special

            if (lastComboCount < combo.Length)
                ExecuteCombo(FindCombo());
        }
    }

    private ScriptableAbility FindCombo()
    {
        foreach (var ability in abilities)
        {
            if (combo.ToString().EndsWith(ability.combo) && Stamina >= ability.staminaCost && Energy >= ability.energyCost)
            {
                return ability;
            }
        }
        return null;
    }

    private void UpdateInputs()
    {
        horizontal = 0;
        vertical = 0;

        if (canMove)
        {
            horizontal = Input.GetAxisRaw("Horizontal");
            vertical = Input.GetAxisRaw("Vertical");

            if (horizontal != 0 && vertical != 0)
            {
                horizontal /= Mathf.Sqrt(2);
                vertical /= Mathf.Sqrt(2);
            }

            walking = Input.GetKey(KeyCode.LeftShift);
        }
    }
}
