from setuptools import setup, find_packages

setup(
    name="StudentPerformanceAnalysis",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "plotly",
        "streamlit"
    ],
    python_requires=">=3.8",
    description="A machine learning project to analyze and predict student performance",
    author="Your Name",
    license="MIT",
)
