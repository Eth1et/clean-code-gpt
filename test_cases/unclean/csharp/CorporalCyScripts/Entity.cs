using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

public abstract class Entity : MonoBehaviour
{
    [Header("Stats")]
    [SerializeField] internal protected float maxHealth = 100f;      [Space(3)]
    [SerializeField] internal protected float maxStamina = 50f;
    [SerializeField] protected float staminaRegen = 1f;              [Space(3)]
    [SerializeField] internal protected float maxEnergy = 20f;
    [SerializeField] protected float energyRegen = .3f;              [Space(3)]
    [Range(0, .3f), SerializeField] protected float movementSmoothing = .05f;
    [SerializeField] protected float walkingSpeed = 50f;
    [SerializeField] protected float runningSpeed = 90f;             [Space(3)] 
    [SerializeField] protected float attackDelay = 0.08f;  // Minimum delay between 2 inputs
    [SerializeField] protected float comboResetTime = .5f;

    [Space(10), Header("References")]
    [SerializeField] protected IKHandler ik;   // Inverse - Kinematics animation handler
    [SerializeField] protected Collider2D playerCollider;
    [SerializeField] protected Collider2D attackCollider;
    [SerializeField] protected List<ScriptableAbility> abilities; // Contains all SO of the abilities
    protected Animator animator;
    protected SpriteRenderer spriteRenderer, ikSpriteRenderer;
    protected Rigidbody2D rb;

    [Space(10), Header("State")]
    [SerializeField] protected Vector2 targetPosition = Vector2.zero;
    protected StringBuilder combo;
    protected ScriptableAbility activeAbility = null;
    protected Vector2 previousProgress = Vector2.zero;
    protected Vector3 velocity = Vector3.zero;

    internal float Health { get => _health; set { _health = Math.Clamp(value, 0, maxHealth); if (_health < 1) Die(); } }
    internal float Stamina { get => _stamina; set { _stamina = Math.Clamp(value, 0, maxStamina); } }
    internal float Energy { get => _energy; set { _energy = Math.Clamp(value, 0, maxEnergy); } }

    protected float _health;
    protected float _stamina;
    protected float _energy;
    protected float nextAttack;
    protected float cancelCombo;
    protected float horizontal;
    protected float vertical;

    protected bool alive = true;
    protected bool canMove = true;
    protected bool inAttack = false;
    protected bool facingRight = true;
    protected bool walking = false;

    protected virtual void Awake()
    {
        animator = GetComponent<Animator>();
        spriteRenderer = GetComponent<SpriteRenderer>();
        ikSpriteRenderer = ik.gameObject.GetComponent<SpriteRenderer>();
        rb = GetComponent<Rigidbody2D>();

        // Ensuring that combos execute instead of 1 button abilities
        abilities.Sort(new ComboLengthReverseComparer());
    }

    protected virtual void Start()
    {
        spriteRenderer.enabled = false;
        ikSpriteRenderer.enabled = true;
        Health = maxHealth;
        Stamina = maxStamina;
        Energy = maxEnergy;
        combo = new StringBuilder();
    }

    protected virtual void Update()
    {
        if (!inAttack && alive)
        {
            Stamina += staminaRegen * Time.deltaTime;
            Energy += energyRegen * Time.deltaTime;
            previousProgress = Vector2.zero;
        }

        ik.Dissolve();
    }

    protected virtual void FixedUpdate()
    {
        if (!inAttack)
        {
            if(canMove)
            {
                Move(horizontal * Time.fixedDeltaTime, vertical * Time.fixedDeltaTime);
            }
        }
        else
        {
            ApplyAbilityMovement();
        }
    }

    protected virtual void LateUpdate()
    {
        if (!inAttack)
        {
            ik.AnimateCharacter((horizontal != 0 || vertical != 0), walking);
        }
    }

    protected void Move(float x_Move, float y_Move)
    {
        float factor = walking ? walkingSpeed : runningSpeed;

        Vector3 targetVelocity = new Vector2(x_Move, y_Move) * factor;

        //smoothing it out and applying it to the character
        rb.velocity = Vector3.SmoothDamp(rb.velocity, targetVelocity, ref velocity, movementSmoothing);

        if ((x_Move > 0 && !facingRight) || (x_Move < 0 && facingRight))
        {
            ik.Flip();
            facingRight = !facingRight;
        }
    }

    protected void ApplyAbilityMovement()
    {
        targetPosition.x *= facingRight ? 1 : -1;
        Vector2 displacement = targetPosition - previousProgress;

        rb.MovePosition(new Vector2(transform.position.x, transform.position.y) + displacement);

        if ((displacement.x > 0 && !facingRight) || (displacement.x < 0 && facingRight))
        {
            ik.Flip();
            facingRight = !facingRight;
        }

        previousProgress = displacement + previousProgress;
    }

    protected void ExecuteCombo(ScriptableAbility ability)
    {
        if(ability == null) return;

        Stamina -= ability.staminaCost;
        Energy -= ability.energyCost;
        activeAbility = ability;

        InvertMode();
        animator.Play(ability.animationClip.name);

        if (ability.combo.Length > 1) // Prevents default attacks from clearing the combo
            combo.Clear();

        cancelCombo = Time.time + comboResetTime + ability.animationClip.length;
        nextAttack = Time.time + attackDelay + ability.animationClip.length;
    }

    /// <summary>
    /// Changes from using sprite sheet animation in combat mode => Inverse kinematics and out of combat mode
    /// </summary>
    protected void InvertMode()
    {
        animator.StopPlayback();
        previousProgress = Vector2.zero;
        animator.enabled = !animator.enabled;
        spriteRenderer.enabled = !spriteRenderer.enabled;
        ikSpriteRenderer.enabled = !ikSpriteRenderer.enabled;
        inAttack = !inAttack;
        gameObject.layer = gameObject.layer == 10? 9 : 10;
    }

    public void EndPhase(int phase)
    {
        activeAbility.ApplyPhaseEffects(this, phase);
    }

    public void EndAnimation(int lastPhase)
    {
        EndPhase(lastPhase);
        InvertMode();
    }

    protected void Die()
    {
        alive = false;
        animator.StopPlayback();
        ik.StartDissolve();
    }

    // Draw Developement Features
    protected void OnDrawGizmosSelected()
    {
        Vector3 targetGlobalPos = transform.position;
        targetGlobalPos.y += targetPosition.y;
        targetGlobalPos.x += (facingRight ? 1 : -1) * targetPosition.x;

        Gizmos.color = Color.red;
        Gizmos.DrawSphere(targetGlobalPos, .25f);
        Gizmos.DrawLine(transform.position, targetGlobalPos);
    }
}
