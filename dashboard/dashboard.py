# dashboard/dashboard.py
import sys
import os
import streamlit as st
import pandas as pd

# --- Fix module path for scripts folder ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Import modular scripts ---
from scripts import load_data, data_cleaning, feature_engineering, encode_features, model_building, feature_importance

# --- Page Config ---
st.set_page_config(
    page_title="Student Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.title("🎓 Student Performance Analytics Dashboard")
st.markdown("""
Welcome! This dashboard allows you to analyze student performance data, 
compare demographics, visualize feature importance, and predict the performance of a single student.
""")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Step 1: Load & clean
    df = load_data.load_csv(uploaded_file)
    df = data_cleaning.clean_data(df)
    df = feature_engineering.add_features(df)

    # --- Top Metrics ---
    st.subheader("📊 Key Metrics")
    total_students = df.shape[0]
    avg_score = df["average_score"].mean().round(2)
    perf_counts = df["performance_category"].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Average Score", avg_score)
    col3.metric("High Performers", perf_counts.get("high",0))

    # --- Tabs ---
    tabs = st.tabs(["Data Overview", "Comparative Analysis", "Feature Importance", "Predict a Student"])

    # --- Tab 1: Data Overview ---
    with tabs[0]:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Summary Statistics")
        st.write(df.describe())

        st.subheader("Missing Values & Duplicates")
        col1, col2 = st.columns(2)
        col1.write(df.isnull().sum())
        col2.write(df.duplicated().sum())

    # --- Tab 2: Comparative Analysis ---
    with tabs[1]:
        st.subheader("Average Scores by Demographics")
        demo_cols = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]

        for i in range(0, len(demo_cols), 2):
            cols = st.columns(2)
            for j, col_name in enumerate(demo_cols[i:i+2]):
                chart_data = df.groupby(col_name)["average_score"].mean().reset_index()
                cols[j].bar_chart(data=chart_data.set_index(col_name))

        st.subheader("Performance Category Distribution by Demographics")
        for i in range(0, len(demo_cols), 2):
            cols = st.columns(2)
            for j, col_name in enumerate(demo_cols[i:i+2]):
                perf_dist = pd.crosstab(df[col_name], df["performance_category"])
                cols[j].bar_chart(perf_dist)

    # --- Tab 3: Feature Importance ---
    with tabs[2]:
        st.subheader("Feature Importance")
        X, y = encode_features.encode_features(df)
        clf = model_building.train_random_forest(X, y)
        feat_imp_df = feature_importance.plot_feature_importance(clf, X)

        st.write("Top Features Influencing Performance")
        st.dataframe(feat_imp_df.head(10))

    # --- Tab 4: Predict a Single Student ---
    with tabs[3]:
        st.subheader("Predict a Student's Performance")

        with st.form("predict_form"):
            gender = st.selectbox("Gender", ["female", "male"])
            race = st.selectbox("Race/Ethnicity", ["group A","group B","group C","group D","group E"])
            parent_edu = st.selectbox("Parental Level of Education",
                                      ["some high school","high school","some college","associate's degree","bachelor's degree","master's degree"])
            lunch = st.selectbox("Lunch Type", ["standard","free/reduced"])
            prep_course = st.selectbox("Test Preparation Course", ["none","completed"])
            math_score = st.number_input("Math Score", min_value=0, max_value=100, value=70)
            reading_score = st.number_input("Reading Score", min_value=0, max_value=100, value=70)
            writing_score = st.number_input("Writing Score", min_value=0, max_value=100, value=70)

            submitted = st.form_submit_button("Predict")
            if submitted:
                student_df = pd.DataFrame([{
                    "gender": gender,
                    "race/ethnicity": race,
                    "parental level of education": parent_edu,
                    "lunch": lunch,
                    "test preparation course": prep_course,
                    "math score": math_score,
                    "reading score": reading_score,
                    "writing score": writing_score
                }])
                
                # Feature engineering + encoding
                student_df = feature_engineering.add_features(student_df)
                X_student, _ = encode_features.encode_features(student_df)
                X_student = X_student.reindex(columns=X.columns, fill_value=0)
                
                # Prediction
                prediction = model_building.predict(clf, X_student)
                mapping = {0:"low", 1:"medium", 2:"high"}
                st.success(f"Predicted Performance: {mapping[prediction[0]]}")
