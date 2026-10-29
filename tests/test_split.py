import pandas as pd
from src.data.split import chia_du_lieu

def test_split_disjoint_and_deterministic():
    df = pd.DataFrame({'issue_desc':[f'description {i}' for i in range(120)],'issue_category':['PIN']*60+['SAC']*60})
    a=chia_du_lieu(df)
    b=chia_du_lieu(df)
    assert [len(x) for x in a]==[84,18,18]
    assert [x['issue_desc'].tolist() for x in a]==[x['issue_desc'].tolist() for x in b]
    assert len(set(a[0]['issue_desc']) & set(a[2]['issue_desc']))==0
