import pandas as pd

def encode_features(df, target_col="performance_category"):
    """One-hot encode categorical columns and return X, y"""
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    if target_col in categorical_cols:
        categorical_cols.remove(target_col)

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Map target column if it exists
    if target_col in df_encoded.columns:
        y = df_encoded[target_col].map({"low":0, "medium":1, "high":2})
        X = df_encoded.drop(target_col, axis=1)
    else:
        X = df_encoded.copy()
        y = None

    return X, y
