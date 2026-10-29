
from pathlib import Path

import joblib
import numpy as np

from src.features.text import lam_sach


MIN_LENGTH = 10
MIN_WORDS = 2


def load_model(path="artifacts/warranty_model.joblib"):
    if not Path(path).is_file():
        raise FileNotFoundError(
            f"Chưa có mô hình: {path}. Hãy chạy train."
        )
    # Chỉ tải Joblib do dự án tự tạo, không tải file không tin cậy.
    return joblib.load(path)


def validate_description(description):
    """Kiểm tra mô tả trước khi dự đoán."""
    if not isinstance(description, str):
        raise ValueError("Mô tả lỗi phải là chuỗi văn bản.")

    if not description.strip():
        raise ValueError("Vui lòng nhập mô tả lỗi.")

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

    words = [
        word for word in cleaned.split()
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
    threshold = float(bundle.get("nguong_tin_cay", 0.70))

    classes = [str(value) for value in model.classes_]

    confidence = None
    score_type = "unavailable"
    scores = []

    if hasattr(model, "predict_proba"):
        probabilities = np.asarray(
            model.predict_proba(X)[0],
            dtype=float,
        )

        if len(probabilities) != len(classes):
            raise ValueError(
                "Số xác suất không khớp số nhãn."
            )

        if not np.all(np.isfinite(probabilities)):
            raise ValueError(
                "Mô hình trả về xác suất không hợp lệ."
            )

        score_type = "probability"
        confidence = float(
            probabilities[classes.index(label)]
        )

        scores = [
            {
                "label": name,
                "score": float(value),
            }
            for name, value in zip(classes, probabilities)
        ]

    elif hasattr(model, "decision_function"):
        raw_scores = np.asarray(
            model.decision_function(X)
        )

        if raw_scores.ndim == 2:
            raw_scores = raw_scores[0]

        # Với phân loại nhị phân, sklearn trả về một
        # decision score; chuyển về hai giá trị đối nhau.
        if len(classes) == 2 and raw_scores.ndim == 0:
            value = float(raw_scores)
            raw_scores = np.array([-value, value])

        if len(raw_scores) != len(classes):
            raise ValueError(
                "Số điểm quyết định không khớp số nhãn."
            )

        score_type = "decision"

        scores = [
            {
                "label": name,
                "score": float(value),
            }
            for name, value in zip(classes, raw_scores)
        ]

    scores.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "label": label,
        "confidence": confidence,
        "needs_review": (
            confidence is None or confidence < threshold
        ),
        "confidence_calibrated": False,
        "score_type": score_type,
        "scores": scores,
    }
