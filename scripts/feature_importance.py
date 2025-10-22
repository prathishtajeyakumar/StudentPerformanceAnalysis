# scripts/feature_importance.py
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_feature_importance(model, X):
    """
    Plot feature importance for Random Forest model inside Streamlit
    and return the sorted DataFrame.
    
    Parameters:
    - model: trained RandomForestClassifier
    - X: feature DataFrame used to train the model
    """
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({
        "feature": X.columns,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    # Plot horizontal bar chart
    plt.figure(figsize=(10,6))
    plt.barh(feat_imp_df["feature"], feat_imp_df["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance")
    
    # Render the plot in Streamlit
    st.pyplot(plt.gcf())
    
    return feat_imp_df
