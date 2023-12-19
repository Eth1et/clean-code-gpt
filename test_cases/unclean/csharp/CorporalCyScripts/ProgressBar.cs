using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class ProgressBar : MonoBehaviour
{
    [SerializeField] private RectTransform progressRect;
    [SerializeField] private RectTransform barRect;
    [SerializeField] private TMP_Text text;
    [SerializeField] private Canvas canvas;
    private RectTransform rectTransform;

    private void Awake()
    {
        rectTransform = GetComponent<RectTransform>();
    }

    internal void SetProgress(float value, float maxValue)
    {
        progressRect.localScale = new Vector3(value/maxValue, 1, 1);
        text.text = ((int)value).ToString();

        barRect.localScale = new Vector3(Mathf.Min(maxValue / barRect.rect.width, 1), 1, 1);

        LayoutRebuilder.MarkLayoutForRebuild(rectTransform);
    }
}
