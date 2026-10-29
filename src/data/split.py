from sklearn.model_selection import train_test_split

def chia_du_lieu(df, nhan='issue_category', hat_giong=42):
    counts = df[nhan].value_counts()
    if len(counts) < 2 or (counts < 7).any():
        raise ValueError('Cần ít nhất 2 nhãn và tối thiểu 7 mẫu/nhãn để chia phân tầng 70/15/15 ổn định.')
    train, temp = train_test_split(df, test_size=0.30, random_state=hat_giong, stratify=df[nhan])
    val, test = train_test_split(temp, test_size=0.50, random_state=hat_giong, stratify=temp[nhan])
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)
