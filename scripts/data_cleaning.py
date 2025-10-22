def clean_data(df):
    """Clean data: handle missing values, duplicates, basic preprocessing"""
    # Drop duplicates
    df = df.drop_duplicates()
    # Fill missing values if any (example: forward fill)
    df = df.fillna(method='ffill')
    return df
