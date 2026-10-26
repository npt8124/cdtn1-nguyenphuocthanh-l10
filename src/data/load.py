from pathlib import Path
import pandas as pd
from src.features.text import normalize_text

LABELS = ("MAN_HINH", "PIN", "SAC", "PHAN_MEM", "NUOC_VAO", "KHAC")
REQUIRED = {"desc_id", "issue_desc", "issue_category", "center_id"}
DEFAULT_CSV = Path("src/data/mau/issue_descriptions.csv")

def load_dataset(path=DEFAULT_CSV):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu: {path.resolve()}")
    df = pd.read_csv(path, encoding="utf-8-sig", dtype={"issue_desc": "string", "issue_category": "string"})
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV thiếu cột: {', '.join(sorted(missing))}")
    df = df.copy()
    df["issue_desc"] = df["issue_desc"].fillna("").map(normalize_text)
    df["issue_category"] = df["issue_category"].fillna("").str.strip().str.upper()
    df = df[(df.issue_desc.str.len() >= 3) & df.issue_category.isin(LABELS)]
    # Identical text with conflicting labels is ambiguous: exclude from evaluation/training.
    conflicts = df.groupby("issue_desc").issue_category.nunique()
    ambiguous = set(conflicts[conflicts > 1].index)
    df = df[~df.issue_desc.isin(ambiguous)]
    df = df.drop_duplicates(subset=["issue_desc", "issue_category"]).reset_index(drop=True)
    if df.empty:
        raise ValueError("Không còn bản ghi hợp lệ sau khi làm sạch.")
    return df
