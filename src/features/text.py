import re
import unicodedata

def normalize_text(value: str) -> str:
    """Light normalization, retaining Vietnamese diacritics."""
    value = unicodedata.normalize("NFC", str(value or ""))
    return re.sub(r"\s+", " ", value.strip().lower())
