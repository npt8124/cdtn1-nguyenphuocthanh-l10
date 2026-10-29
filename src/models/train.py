"""python -m src.models.train --config configs/train.yaml"""
import argparse
import hashlib
import json
import random
from pathlib import Path
import joblib
import numpy as np
import yaml
from sklearn.metrics import f1_score
from sklearn.svm import LinearSVC
from src.data.load import LABELS, load_dataset
from src.data.split import chia_du_lieu
from src.features.text import lam_sach, tao_vectorizer
from src.models.baseline import tao_dummy, tao_logistic
from src.evaluate import danh_gia
from sklearn.metrics import accuracy_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/train.yaml')
    args = parser.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    seed = int(cfg['hat_giong'])
    random.seed(seed)
    np.random.seed(seed)
    path = Path(cfg['duong_dan_du_lieu'])
    df, stats = load_dataset(path, cfg.get('cot_van_ban','issue_desc'), cfg.get('cot_nhan','issue_category'))
    # Trùng văn bản sau chuẩn hóa gây leakage giữa các tập; bỏ trùng trước khi chia.
    df['_clean'] = df['issue_desc'].map(lam_sach)
    df = df[df['_clean'].ne('')].copy()
    conflicts = df.groupby('_clean')['issue_category'].nunique()
    if (conflicts > 1).any():
        print(f'Cảnh báo: {(conflicts > 1).sum()} mô tả có nhãn mâu thuẫn; loại khỏi huấn luyện.')
        df = df[~df['_clean'].isin(conflicts[conflicts > 1].index)]
    df = df.drop_duplicates(subset=['_clean']).reset_index(drop=True)
    train, val, test = chia_du_lieu(df, hat_giong=seed)
    vectorizer = tao_vectorizer(cfg['min_df'], cfg['max_features'], cfg['ngram_range'])
    X_train = vectorizer.fit_transform(train['_clean'])
    X_val = vectorizer.transform(val['_clean'])
    X_test = vectorizer.transform(test['_clean'])
    y_train, y_val, y_test = train['issue_category'], val['issue_category'], test['issue_category']
    # Tất cả lựa chọn siêu tham số / mô hình dựa trên VALIDATION, không dùng TEST.
    candidates = []
    for C in cfg['C_thu']:
        candidates.append((f'LogisticRegression_C={C}', tao_logistic(C,seed)))
        candidates.append((f'LinearSVC_C={C}', LinearSVC(C=float(C), class_weight='balanced', random_state=seed, max_iter=5000)))
    
    scores = []
    model_comparison = []

    for name, estimator in candidates:
        estimator.fit(X_train, y_train)

        val_predictions = estimator.predict(X_val)

        score = float(
            f1_score(
                y_val,
                val_predictions,
                labels=LABELS,
                average="macro",
                zero_division=0,
            )
        )

        scores.append((name, estimator, score))

        model_comparison.append({
            "model": name,
            "f1_macro_validation": round(score, 6),
        })

    best_name, best_model, best_val = max(
        scores,
        key=lambda x: x[2]
    )

    model_comparison = sorted(
        model_comparison,
        key=lambda item: item["f1_macro_validation"],
        reverse=True,
    )

    # TEST chỉ đánh giá cuối cùng; cả baseline đều huấn luyện trên TRAIN.
    dummy = tao_dummy().fit(X_train, y_train)
    logistic = tao_logistic(1.0, seed).fit(X_train, y_train)

    # Đánh giá baseline trên Validation.
    dummy_val = danh_gia(
        y_val, dummy.predict(X_val), LABELS
    )

    # Đánh giá baseline trên Test.
    dummy_test = danh_gia(
        y_test, dummy.predict(X_test), LABELS
    )

    logistic_test = danh_gia(
        y_test, logistic.predict(X_test), LABELS
    )

    # Thêm DummyClassifier vào bảng so sánh Validation.
    model_comparison.append({
        "model": "DummyClassifier",
        "f1_macro_validation": round(
            float(dummy_val["f1_macro"]), 6
        ),
    })

    model_comparison = sorted(
        model_comparison,
        key=lambda item: item["f1_macro_validation"],
        reverse=True,
    )

    results = {
        'hat_giong':seed,
        'phien_ban_du_lieu':f'{path.name}; sha256={hashlib.sha256(path.read_bytes()).hexdigest()}',
        'so_dong_csv_goc':stats['so_dong_goc'],
        'so_dong_hop_le_truoc_khu_trung':stats['so_dong_hop_le'],
        'so_mau_sau_khu_trung':len(df),
        'so_mau_train':len(train), 'so_mau_val':len(val), 'so_mau_test':len(test),
        'phan_bo_nhan':{k:int(v) for k,v in df['issue_category'].value_counts().sort_index().items()},
        'cau_hinh_vectorizer':{'ngram_range':list(cfg['ngram_range']), 'min_df':cfg['min_df'], 'max_features':cfg['max_features']},
        'chon_mo_hinh_tren_validation':best_name,
        'f1_macro_validation_mo_hinh_chinh':round(best_val,6),        
        "f1_macro_baseline_da_so": dummy_test["f1_macro"],
        "accuracy_baseline_da_so": dummy_test["accuracy"],
        "f1_macro_baseline_tfidf_logistic":
            logistic_test["f1_macro"],
        "accuracy_baseline_tfidf_logistic":
            logistic_test["accuracy"],
        "phan_bo_nhan_theo_tap": {
            "train": {
                label: int((y_train == label).sum())
                for label in LABELS
            },
            "validation": {
                label: int((y_val == label).sum())
                for label in LABELS
            },
            "test": {
                label: int((y_test == label).sum())
                for label in LABELS
            },
        },
        "so_sanh_mo_hinh_validation": model_comparison,
        "nhan": list(LABELS),
    }
    final = danh_gia(y_test,best_model.predict(X_test),LABELS)
    label_status = {}

    for label in LABELS:
        report = final["classification_report"].get(label, {})

        support = int(report.get("support", 0))
        precision = float(report.get("precision", 0))
        recall = float(report.get("recall", 0))
        f1 = float(report.get("f1-score", 0))

        if support == 0:
            status = "KHONG_CO_DU_LIEU"
            message = "Nhãn không có mẫu trong tập Test."
        elif f1 == 0:
            status = "F1_BANG_0"
            message = (
                "Nhãn có dữ liệu nhưng F1 bằng 0; "
                "cần kiểm tra khả năng nhận diện."
            )
        else:
            status = "CO_DU_LIEU"
            message = "Nhãn có dữ liệu trong tập Test."

        label_status[label] = {
            "support": support,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "status": status,
            "message": message,
        }

    results["trang_thai_tung_nhan"] = label_status
    results.update({'f1_macro_mo_hinh_chinh':final['f1_macro'], 'accuracy_mo_hinh_chinh':final['accuracy'], 'f1_theo_nhan':final['f1_theo_nhan'], 'confusion_matrix':final['confusion_matrix'], 'classification_report':final['classification_report']})
    Path('reports').mkdir(exist_ok=True)
    Path('artifacts').mkdir(exist_ok=True)
    Path('reports/metrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    joblib.dump({'vectorizer':vectorizer,'model':best_model,'labels':list(LABELS),'nguong_tin_cay':float(cfg.get('nguong_tin_cay',0.70))},'artifacts/warranty_model.joblib')
    print('Đã lưu reports/metrics.json và artifacts/warranty_model.joblib')
    print(f"Mô hình: {best_name}; Validation Macro F1: {best_val:.4f}; Test Macro F1: {final['f1_macro']:.4f}")
    if best_name.startswith('LinearSVC'):
        print('Lưu ý: LinearSVC không có xác suất chuẩn; độ tin cậy cần hiệu chuẩn trước khi sử dụng ngưỡng 0.70.')

if __name__=='__main__':
    main()
