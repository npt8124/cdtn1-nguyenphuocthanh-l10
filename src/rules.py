from src.data.load import LABELS

PRIORITIES = ("CAO", "TRUNG_BINH", "THAP")

def suggest_priority(category: str, description: str = "") -> str:
    """Illustrative, editable business rules, not ML output or warranty decisions."""
    if category not in LABELS:
        raise ValueError("Nhóm sự cố không hợp lệ")
    if category == "NUOC_VAO":
        return "CAO"
    if category in {"PIN", "SAC", "MAN_HINH"}:
        return "TRUNG_BINH"
    return "THAP"
