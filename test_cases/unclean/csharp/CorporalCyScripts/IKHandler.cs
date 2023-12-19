using System.Collections;
using UnityEngine;

public class IKHandler : MonoBehaviour
{
    [SerializeField] private float dissolveSpeed = .5f;

    [SerializeField] private Animator hairAnimator;
    private Animator bodyAnimator;
    private Material material;

    private float fade = 1f;
    private bool isDissolving = false;

    private void Awake()
    {
        bodyAnimator = GetComponent<Animator>();
        material = GetComponent<SpriteRenderer>().material;
    }

    public void AnimateHair(bool running)
    {
        hairAnimator.SetBool("isRunning", running);
    }

    public void AnimateCharacter(bool moving, bool walking)
    {
        if (moving)
        {
            if (walking)
            {
                bodyAnimator.SetBool("isWalking", true);
                bodyAnimator.SetBool("isRunning", false);
            }
            else
            {
                bodyAnimator.SetBool("isWalking", false);
                bodyAnimator.SetBool("isRunning", true);
            }
        }
        else
        {
            bodyAnimator.SetBool("isWalking", false);
            bodyAnimator.SetBool("isRunning", false);
        }

        AnimateHair(!walking && moving);
    }

    public void Flip()
    {
        Vector3 scale = transform.parent.localScale;
        scale.x *= -1;
        transform.parent.localScale = scale;
    }

    public void StartDissolve()
    {
        isDissolving = true;
        bodyAnimator.SetTrigger("isDead");
        StartCoroutine(ResetTriggerAfterTime(bodyAnimator, "isDead", 0.001f));
        hairAnimator.SetBool("isDead", true);
    }

    public void Dissolve()
    {
        if (isDissolving)
        {
            fade -= Time.deltaTime * dissolveSpeed;

            if (fade <= 0f)
            {
                fade = 0f;
                isDissolving = false;
            }
        }

        material.SetFloat("_Fade", fade);
    }

    private IEnumerator ResetTriggerAfterTime(Animator animator, string triggerName, float delay)
    {
        yield return new WaitForSeconds(delay);
        animator.ResetTrigger(triggerName);
    }
}
