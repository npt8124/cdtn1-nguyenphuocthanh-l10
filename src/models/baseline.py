from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression

def tao_dummy():
    return DummyClassifier(strategy='most_frequent')

def tao_logistic(C=1.0, hat_giong=42):
    return LogisticRegression(C=float(C), max_iter=1000, class_weight='balanced', random_state=hat_giong)
