import pandas as pd

def add_features(df):
    """Add average score and performance category"""
    if all(col in df.columns for col in ["math score", "reading score", "writing score"]):
        df["average_score"] = df[["math score", "reading score", "writing score"]].mean(axis=1)
        bins = [0, 60, 80, 100]
        labels = ["low", "medium", "high"]
        df["performance_category"] = pd.cut(df["average_score"], bins=bins, labels=labels)
    return df
