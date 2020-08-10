from sklearn.linear_model import LogisticRegression
from joblib import load

def load_predict(data, model_path):
    clf = load(model_path)

    y_pred = clf.predict(data)

    return y_pred, clf

def predict(data, clf):
    y_pred = clf.predict(data)

    return y_pred