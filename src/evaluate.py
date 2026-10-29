from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

def danh_gia(y_true, y_pred, labels):
    return {
        'f1_macro': round(float(f1_score(y_true, y_pred, labels=labels, average='macro', zero_division=0)), 6),
        'accuracy': round(float(accuracy_score(y_true, y_pred)), 6),
        'f1_theo_nhan': {k:round(float(v), 6) for k,v in zip(labels, f1_score(y_true, y_pred, labels=labels, average=None, zero_division=0))},
        'confusion_matrix': confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        'classification_report': classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0),
    }
