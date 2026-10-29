
from pathlib import Path
import re

import joblib
import numpy as np

from src.features.text import lam_sach


MIN_LENGTH = 10
MIN_WORDS = 2


def load_model(path="artifacts/warranty_model.joblib"):
    if not Path(path).is_file():
        raise FileNotFoundError(
            f"Chưa có mô hình: {path}. Hãy chạy train.") 
    return joblib.load(path) # Chỉ tải file joblib do chính bạn tạo, không tải nguồn không tin cậy.

def validate_description(description):
    """Kiểm tra mô tả đầu vào trước khi dự đoán."""
    if not isinstance(description, str):
        raise ValueError("Mô tả lỗi phải là chuỗi văn bản.")
    if not description.strip():
        raise ValueError("Vui lòng nhập mô tả lỗi.")

    # Kiểm tra tỷ lệ ký tự đặc biệt trên chuỗi gốc
    raw = description.strip()
    special_count = sum(
        not ch.isalnum() and not ch.isspace()
        for ch in raw
    )
    if special_count / len(raw) > 0.4:
        raise ValueError(
            "Mô tả chứa quá nhiều ký tự đặc biệt."
        )
    cleaned = lam_sach(description)
    if len(cleaned) < MIN_LENGTH:
        raise ValueError(
            f"Mô tả lỗi phải có ít nhất {MIN_LENGTH} ký tự."
        )

    # Chỉ đếm các từ chứa chữ cái, không đếm token số
    words = [
        word
        for word in cleaned.split()
        if any(ch.isalpha() for ch in word)
    ]
    if len(words) < MIN_WORDS:
        raise ValueError(
            f"Mô tả lỗi phải có ít nhất {MIN_WORDS} từ."
        )
    return cleaned

def predict(bundle, description):
    cleaned = validate_description(description)
    X = bundle["vectorizer"].transform([cleaned])
    model = bundle["model"]
    label = str(model.predict(X)[0])
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)[0]
        confidence = float(np.max(probabilities))
    else:
        confidence = None

    threshold = bundle.get("nguong_tin_cay", 0.70)
    return {
        "label": label,
        "confidence": confidence,
        "needs_review": (
            confidence is None or confidence < threshold
        ),
        "confidence_calibrated": False,
    }
