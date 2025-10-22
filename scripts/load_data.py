import pandas as pd

def load_csv(file):
    """Load CSV file into a DataFrame"""
    df = pd.read_csv(file)
    return df
