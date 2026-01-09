import pandas as pd
import pytest
import os

def test_data_exists():
    path = '../data/processed/sales_clean.csv'
    assert os.path.exists(path), f"Data missing: {path}"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "Empty dataset"
    assert 'total_price' in df.columns
    assert df['total_price'].sum() > 0
