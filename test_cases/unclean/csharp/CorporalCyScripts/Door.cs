using UnityEngine;

public class Door : MonoBehaviour
{
    private Animator animator;

    private void Awake()
    {
        animator = GetComponent<Animator>();
        animator.SetBool("open", false);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.transform.CompareTag("Player"))
        {
            animator.SetBool("open",true);
        }
    }
    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.transform.CompareTag("Player"))
        {
            animator.SetBool("open", false);
        }
    }
}
