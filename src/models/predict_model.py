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

def extract_features_predict(path, clf, exif_tags = None):
    # if none given, set default values
    if exif_tags == None:
        exif_tags = {
            'exposure_time': 0x829a,
            'shutter_speed': 0x9201,
            'brightness': 0x9203,
            'iso_speed': 0x8827
        }
    feature_cols = exif_tags.keys()

    # load data
    data = build_features.get_exif_data(path, exif_tags)

    # classify images
    y_pred = clf.predict(data[feature_cols])

    # add prediction to data frame
    data['prediction'] = y_pred

    return data