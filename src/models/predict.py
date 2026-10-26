from pathlib import Path
import joblib
from src.features.text import normalize_text

DEFAULT_MODEL = Path("models/warranty_classifier.joblib")
THRESHOLD = 0.70  # Proposed; calibrate using validation set before production.

def load_model(path=DEFAULT_MODEL):
    if not Path(path).is_file():
        raise FileNotFoundError("Chưa có mô hình. Chạy: python -m src.models.train")
    # Only load trusted local model files; joblib uses pickle.
    return joblib.load(path)

def predict(model, description):
    text = normalize_text(description)
    if len(text) < 3:
        raise ValueError("Vui lòng nhập mô tả lỗi tối thiểu 3 ký tự.")
    probs = model.predict_proba([text])[0]
    classes = model.classes_
    index = int(probs.argmax())
    return {"label": str(classes[index]), "confidence": float(probs[index]),
            "needs_review": float(probs[index]) < THRESHOLD,
            "scores": {str(label): float(prob) for label, prob in zip(classes, probs)}}
