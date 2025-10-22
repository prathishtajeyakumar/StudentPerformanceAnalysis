from sklearn.ensemble import RandomForestClassifier

def train_random_forest(X, y):
    """Train Random Forest Classifier"""
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return clf

def predict(clf, X_new):
    """Predict using trained model"""
    return clf.predict(X_new)
