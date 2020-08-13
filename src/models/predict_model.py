from sklearn.linear_model import LogisticRegression
from joblib import load

from src.features import build_features

def load_model(model_path):
    return load(model_path)

def load_predict(data, model_path):
    clf = load_model(model_path)

    y_pred = clf.predict(data)

    return y_pred, clf

def predict(data, clf):
    y_pred = clf.predict(data)

    return y_pred