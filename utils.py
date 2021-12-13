def replace_str(text, dic):
    """Replace text based on dict provided."""

    for i, j in dic.items():
        text = text.replace(i, j)
    return text
