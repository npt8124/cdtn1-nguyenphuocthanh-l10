import re
from sklearn.feature_extraction.text import TfidfVectorizer

PHONE = re.compile(r'(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){9}(?!\d)')
SERIAL = re.compile(r'\bSN[\s-]*\d+\b', flags=re.IGNORECASE)
EMAIL = re.compile(r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b')

def lam_sach(s):
    """Không bỏ dấu; ẩn email, điện thoại, serial. Tên riêng cần rà soát bổ sung."""
    if s is None:
        return ''
    s = str(s).lower()
    s = EMAIL.sub(' emailtoken ', s)
    s = PHONE.sub(' sdttoken ', s)
    s = SERIAL.sub(' serialtoken ', s)
    s = re.sub(r'[^\w\s]', ' ', s, flags=re.UNICODE)
    s = re.sub(r'\s+', ' ', s).strip()
    return (s.replace('emailtoken', '<EMAIL>')
             .replace('sdttoken', '<SDT>')
             .replace('serialtoken', '<SERIAL>'))

def tao_vectorizer(min_df=2, max_features=20000, ngram_range=(1, 2)):
    return TfidfVectorizer(ngram_range=tuple(ngram_range), min_df=min_df, max_features=max_features, lowercase=False, token_pattern=r'(?u)\b\w+\b')
