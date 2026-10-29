from pathlib import Path
import pandas as pd

LABELS = ('MAN_HINH', 'PIN', 'SAC', 'PHAN_MEM', 'NUOC_VAO', 'KHAC')

def load_dataset(path, text_col='issue_desc', label_col='issue_category'):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Không tìm thấy CSV: {path.resolve()}')
    df = pd.read_csv(path, encoding='utf-8-sig')
    missing = {text_col, label_col} - set(df.columns)
    if missing:
        raise ValueError(f'Thiếu cột bắt buộc: {sorted(missing)}; cột hiện có: {list(df.columns)}')
    df = df[[text_col, label_col]].copy()
    before = len(df)
    df = df.dropna(subset=[text_col, label_col])
    df[text_col] = df[text_col].astype(str).str.strip()
    df[label_col] = df[label_col].astype(str).str.strip().str.upper()
    df = df[df[text_col].ne('')]
    bad = sorted(set(df[label_col]) - set(LABELS))
    if bad:
        raise ValueError(f'Nhãn không hợp lệ: {bad}')
    # Không tự xóa trùng lặp tại đây: kiểm tra trùng lặp và tránh leakage trong train.
    if df.empty:
        raise ValueError('Không có dữ liệu hợp lệ.')
    return df.reset_index(drop=True), {'so_dong_goc': before, 'so_dong_hop_le': len(df), 'phan_bo_nhan': {k:int(v) for k,v in df[label_col].value_counts().sort_index().items()}}
