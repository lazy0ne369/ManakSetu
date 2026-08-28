import re


def clean_text(text: str) -> str:
    """Cleans extracted document text by removing excessive whitespace, artifacts, and normalizing quotes."""
    if not text:
        return ""
    # Normalize unicode quotes and dashes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = text.replace("—", " - ").replace("–", " - ")
    # Replace non-breaking spaces
    text = text.replace("\u00a0", " ")
    # Remove control characters except newline and tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)
    # Condense multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Condense multiple spaces
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_is_number(is_str: str) -> str:
    """Normalizes Indian Standard number strings, e.g., 'is2347:2017' -> 'IS 2347:2017'."""
    if not is_str:
        return ""
    clean = is_str.strip()
    match = re.search(r"(?:IS\s*|is\s*)?(\d+(?:\s*\([^\)]+\))?(?:-\d+)?(?::\d{4})?)", clean, re.IGNORECASE)
    if match:
        num_part = match.group(1).strip()
        return f"IS {num_part}"
    return clean
