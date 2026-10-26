import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.data.load import DEFAULT_CSV, LABELS, load_dataset

MODEL_PATH = Path("models/warranty_classifier.joblib")
REPORT_PATH = Path("models/evaluation.json")

def train(csv_path=DEFAULT_CSV):
    df = load_dataset(csv_path)
    counts = df.issue_category.value_counts()
    if len(counts) < 2 or counts.min() < 3:
        raise ValueError("Cần ít nhất 2 lớp và tối thiểu 3 mẫu mỗi lớp để chia tập phân tầng.")
    X_train, X_hold, y_train, y_hold = train_test_split(
        df.issue_desc, df.issue_category, test_size=0.30, random_state=42,
        stratify=df.issue_category)
    X_val, X_test, y_val, y_test = train_test_split(
        X_hold, y_hold, test_size=0.50, random_state=42, stratify=y_hold)
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True, max_features=30000)),
        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit(X_train, y_train)
    # Validation is diagnostic; do not tune on test results.
    val_pred = pipeline.predict(X_val)
    test_pred = pipeline.predict(X_test)
    report = {
        "source_csv": str(csv_path), "created_utc": datetime.now(timezone.utc).isoformat(),
        "records_after_cleaning": len(df), "class_distribution": counts.to_dict(),
        "split": {"train": len(X_train), "validation": len(X_val), "test": len(X_test)},
        "validation_macro_f1": float(f1_score(y_val, val_pred, average="macro")),
        "test_macro_f1": float(f1_score(y_test, test_pred, average="macro")),
        "test_accuracy": float(accuracy_score(y_test, test_pred)),
        "test_classification_report": classification_report(y_test, test_pred, labels=list(LABELS), output_dict=True, zero_division=0),
        "confusion_labels": list(LABELS),
        "test_confusion_matrix": confusion_matrix(y_test, test_pred, labels=list(LABELS)).tolist(),
        "note": "0.70 is a proposed confidence threshold, not a calibrated guarantee. Test set must not guide model selection."
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã huấn luyện {len(df)} bản ghi; Macro F1 test: {report['test_macro_f1']:.3f}")
    print(f"Mô hình: {MODEL_PATH} | Báo cáo: {REPORT_PATH}")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    args = parser.parse_args()
    train(args.csv)
